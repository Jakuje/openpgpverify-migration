#!/usr/bin/python3 -I
"""Phase 2 spec rewrite: %gpgverify -> %openpgpverify (see README "Conversion rules").

Usage: convert.py SPEC INVENTORY.jsonl OUT.spec

Works on the spec text only. Returns notes about anything a human should look
at; raises Unconvertible when the spec needs manual work (raw gpg calls,
rich dependencies around gpg BRs, ...).

Changelog entries are not handled here; that is done when preparing the PR.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import state  # noqa: E402


class Unconvertible(Exception):
    pass


SECTION = re.compile(r'^%(prep|conf|generate_buildrequires|build|install|check|'
                     r'description|package|files|changelog)\b')
COND_OPEN = re.compile(r'^%(if|ifarch|ifnarch|ifos|ifnos)\b')
COND_END = re.compile(r'^%endif\b')
BR_LINE = re.compile(r'^(BuildRequires\s*:\s*)(.*?)(\s*)$', re.I)
# Dependencies replaced by openpgpverify. gnupg2 is handled separately.
DROP = re.compile(r'^(gpgverify|%\{gpgverify\}|(%\{_bindir\}|/usr/bin)/gpgv2?)$')
GNUPG2 = re.compile(r'^(gnupg2?|gpg)$')   # gpg is a provide of gnupg2
OP = re.compile(r'^(<|>|<=|>=|=|==)$')


def split_deps(value):
    """Split a BuildRequires value into dependency strings, keeping versions."""
    tokens = [t for t in re.split(r'[\s,]+', value) if t]
    deps = []
    i = 0
    while i < len(tokens):
        if i + 2 < len(tokens) and OP.match(tokens[i + 1]):
            deps.append(' '.join(tokens[i:i + 3]))
            i += 3
        else:
            deps.append(tokens[i])
            i += 1
    return deps


def rewrite_calls(body):
    """Rename macro calls keeping their exact form."""
    # "%%gpgverify" is an escaped literal in a comment. Rename it too ("# for
    # %%gpgverify" above a BuildRequires), except where the comment is about
    # EL/EPEL, which talks about the old macro on purpose.
    body = '\n'.join(l if re.search(r'\bEL-?\d|epel|rhel', l, re.I)
                     else l.replace('%%gpgverify', '%%openpgpverify')
                     for l in body.split('\n'))
    body, n1 = re.subn(r'(?<!%)%\{gpgverify\}', '%{openpgpverify}', body)
    body, n2 = re.subn(r'(?<!%)%\{\?gpgverify(?=[:}])', '%{?openpgpverify', body)
    body, n3 = re.subn(r'(?<!%)%gpgverify\b', '%openpgpverify', body)
    return body, n1 + n2 + n3


DROPPED = '\x00dropped-br'   # marks a BuildRequires line removed inside %if


def drop_empty_branches(lines):
    """Remove a "%else" branch or a whole "%if" block that contained nothing
    but a BuildRequires we dropped. Pre-existing empty blocks stay untouched."""
    out = []
    for line in lines:
        out.append(line)
        if len(out) >= 3 and out[-2] == DROPPED and COND_END.match(out[-1].strip()):
            opener = out[-3].strip()
            if re.match(r'^%else\b', opener):
                del out[-3:-1]                 # "%else", marker; keep "%endif"
            elif COND_OPEN.match(opener):
                del out[-3:]                   # the whole "%if ... %endif"
    return [l for l in out if l != DROPPED]


# A direct gpgv call that maps 1:1 onto the macro:
#   [CMD |] gpgv[2] [--quiet] --keyring[= ]KEYRING SIGNATURE DATA
RAW_SIMPLE = re.compile(r'^(?P<indent>\s*)(?:(?P<pipe>\S.*?)\s*(?<!\|)\|(?!\|)\s*)?gpgv2?\s+(?:--quiet\s+)?'
                        r'--keyring[= ](?P<k>\S+)\s+(?:--quiet\s+)?(?P<s>\S+)\s+(?P<d>\S+)\s*$')
MANUAL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'manual')


def quote(arg):
    return arg if arg[:1] in '\'"' else "'%s'" % arg


def non_fedora(x):
    """A raw call in the "%else" of a Fedora condition ("%if 0%{?fedora} ||
    0%{?rhel} >= 9 ... %else") is for old EL branches without openpgpverify."""
    return any(re.search(r'fedora.*\| %else$', c) for c in x['conditions'])


def manual_patch(pkg):
    path = os.path.join(MANUAL, pkg + '.patch')
    return path if os.path.exists(path) else None


def rewrite_raw(text, rec):
    """Rewrite direct gpgv calls into %{gpgverify} calls, so that convert()
    can take over (rename, BuildRequires, Release). Only the simple form is
    rewritten; anything else needs a hand-written manual/PKG.patch, which
    turns the spec into one using %{gpgverify}."""
    lines = text.split('\n')
    for x in rec['raw_verify']:
        if non_fedora(x):
            continue
        i = x['line'] - 1
        m = RAW_SIMPLE.match(lines[i])
        if not m:
            raise Unconvertible('raw gpg call needs a manual rewrite: %s' % lines[i].strip())
        data = '--data=-' if m.group('d') == '-' else '--data=%s' % quote(m.group('d'))
        call = "%%{gpgverify} --keyring=%s --signature=%s %s" % (
            quote(m.group('k')), quote(m.group('s')), data)
        lines[i] = m.group('indent') + (m.group('pipe') + ' | ' if m.group('pipe') else '') + call
    return '\n'.join(lines)


SOURCE_TAG = re.compile(r'^Source(\d*)\s*:\s*(\S+)', re.I)
# A command in a comment that fetched or exported the key ("# gpg2 --recv-keys ...",
# "#   $ curl ... | gpg --dearmor > key.gpg").
KEY_CMD = re.compile(r'^#\s*(\$\s*)?(gpg2?|gpgv2?|sq|curl|wget|gpg-wks-client)\s')


def refresh_comment(text, pkg, name, cmds,
                    header='# Refreshed from keyservers/WKD (same keys, newer signatures):'):
    """Put the keyring refresh commands CMDS in the comment above the Source
    line of keyring file NAME, replacing commands that fetched or exported the
    key before (descriptive comment lines stay). Returns (text, note)."""
    lines = text.split('\n')
    # Simple one-word %global/%define values, as used in keyring file names.
    macros = dict(re.findall(r'(?m)^%(?:global|define)\s+(\w+)\s+([^\s%]+)\s*$', text))
    macros['name'] = pkg
    src = None
    for i, line in enumerate(lines):
        m = SOURCE_TAG.match(line)
        if m:
            value = re.sub(r'%\{\??(\w+)\}|%(\w+)\b',
                           lambda x: macros.get(x.group(1) or x.group(2), x.group(0)),
                           m.group(2))
            if value.rsplit('/', 1)[-1] == name:
                src = i
                break
    if src is None:
        return text, 'no Source line for %s; refresh commands only in the PR' % name
    top = src
    while top > 0 and lines[top - 1].startswith('#'):
        top -= 1
    block = lines[top:src]
    keep, at, cont = [], None, False
    for line in block:
        if KEY_CMD.match(line) or cont:
            at = len(keep) if at is None else at
            cont = line.rstrip().endswith('\\')
            continue
        keep.append(line)
    new = [header]
    for c in cmds:
        new.append('#   ' + re.sub(r' \\\n\s*', ' ', c).replace('%', '%%'))
    if at is None:
        at = len(keep)
    lines[top:src] = keep[:at] + new + keep[at:]
    return '\n'.join(lines), None


def convert(text, rec, drop_gnupg2=None):
    """drop_gnupg2: None drops "BR: gnupg2" only for gnupg2_action "remove"
    (no %check); True also for "review" (has %check), False never. With True
    the caller has to prove that the build and its tests work without gnupg2
    (phase1.py gnupg2 check)."""
    if rec['raw_verify']:
        raise Unconvertible('raw gpg/gpgv verification needs a manual rewrite')
    if not rec['calls']:
        raise Unconvertible('no %gpgverify call found')
    notes = []
    m = re.search(r'(?m)^%changelog\b', text)
    body, changelog = (text[:m.start()], text[m.start():]) if m else (text, '')

    lines = body.split('\n')
    out = []
    section = 'preamble'
    depth = 0
    insert_at = None          # index in out where BR: openpgpverify goes
    last_uncond_br = None
    first_section = None
    have_op = rec['br']['openpgpverify']
    m = re.search(r'(?mi)^(BuildRequires\s*:\s*)\S', body)
    br_new = (m.group(1) if m else 'BuildRequires:  ') + 'openpgpverify'
    for line in lines:
        s = line.strip()
        if SECTION.match(s):
            section = SECTION.match(s).group(1)
            if first_section is None and section != 'preamble':
                first_section = len(out)
        elif COND_OPEN.match(s):
            depth += 1
        elif COND_END.match(s):
            depth = max(depth - 1, 0)
        mbr = BR_LINE.match(line) if section in ('preamble', 'package') else None
        if not mbr:
            out.append(line)
            continue
        prefix, value, trail = mbr.groups()
        if depth == 0 and section == 'preamble':
            last_uncond_br = len(out)
        # Rich dependencies start with "(" (pkgconfig(gpgme) is a plain provide).
        if re.search(r'(^|[\s,])\(', value) and re.search(r'gpg|gnupg', value):
            raise Unconvertible('rich dependency mentions gpg: %s' % s)
        deps = split_deps(value)
        keep, dropped = [], []
        for d in deps:
            name = d.split()[0]
            if DROP.match(name):
                dropped.append(d)
            elif GNUPG2.match(name) and drop_gnupg2 is not False and (
                    rec['gnupg2_action'] == 'remove' or
                    drop_gnupg2 and rec['gnupg2_action'] == 'review'):
                dropped.append(d)
            else:
                keep.append(d)
        if not dropped:
            out.append(line)
            continue
        if depth == 0 and insert_at is None:
            insert_at = len(out)
        if depth:
            notes.append('dropped conditional BR: %s' % s)
        if keep:
            out.append(prefix + (', ' if ',' in value else ' ').join(keep) + trail)
            if depth == 0 and insert_at is not None and insert_at == len(out) - 1:
                insert_at += 1
        elif depth:
            out.append(DROPPED)
    if not have_op:
        if insert_at is None:
            if last_uncond_br is not None:
                insert_at = last_uncond_br + 1
            elif first_section is not None:
                insert_at = first_section
                notes.append('no unconditional BuildRequires; BR added before first section')
            else:
                raise Unconvertible('could not find a place for BuildRequires')
        out.insert(insert_at, br_new)
    out = drop_empty_branches(out)
    body, ncalls = rewrite_calls('\n'.join(out))
    if ncalls == 0:
        raise Unconvertible('no macro call rewritten')
    if re.search(r'(?<!%)%\{?\??gpgverify', body.replace('openpgpverify', '')):
        raise Unconvertible('gpgverify still referenced after rewrite')
    if rec['br']['gnupg2'] and (rec['gnupg2_action'] == 'keep' or drop_gnupg2 is False or
                                rec['gnupg2_action'] == 'review' and not drop_gnupg2):
        notes.append('BR gnupg2 kept (%s)' % rec['gnupg2_action'])
    return body + changelog, notes


def main():
    spec, inv_path, out = sys.argv[1:4]
    name = os.path.basename(spec)[:-5]
    rec = state.load_inventory(inv_path)[name]
    with open(spec) as fh:
        text = fh.read()
    try:
        new, notes = convert(text, rec)
    except Unconvertible as e:
        print('unconvertible: %s' % e)
        return 1
    with open(out, 'w') as fh:
        fh.write(new)
    for n in notes:
        print('note: %s' % n)
    return 0


if __name__ == '__main__':
    sys.exit(main())
