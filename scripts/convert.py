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
GNUPG2 = re.compile(r'^gnupg2?$')
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
    body, n1 = re.subn(r'%\{gpgverify\}', '%{openpgpverify}', body)
    body, n2 = re.subn(r'%\{\?gpgverify(?=[:}])', '%{?openpgpverify', body)
    body, n3 = re.subn(r'%gpgverify\b', '%openpgpverify', body)
    return body, n1 + n2 + n3


def convert(text, rec):
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
            elif GNUPG2.match(name) and rec['gnupg2_action'] == 'remove':
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
    if not have_op:
        if insert_at is None:
            if last_uncond_br is not None:
                insert_at = last_uncond_br + 1
            elif first_section is not None:
                insert_at = first_section
                notes.append('no unconditional BuildRequires; BR added before first section')
            else:
                raise Unconvertible('could not find a place for BuildRequires')
        out.insert(insert_at, 'BuildRequires:  openpgpverify')
    body, ncalls = rewrite_calls('\n'.join(out))
    if ncalls == 0:
        raise Unconvertible('no macro call rewritten')
    if re.search(r'%\{?\??gpgverify', body.replace('openpgpverify', '')):
        raise Unconvertible('gpgverify still referenced after rewrite')
    if rec['rhel_conditional']:
        notes.append('rhel conditional: use the README template for the PR')
    if rec['gnupg2_action'] in ('review', 'keep'):
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
