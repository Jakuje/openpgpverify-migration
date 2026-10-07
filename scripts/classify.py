#!/usr/bin/python3 -I
"""Phase 0: classify Fedora specs by how they verify upstream source signatures.

Usage: classify.py SPECDIR OUT.jsonl [SRPM_SIZES]

SPECDIR      extracted rpm-specs-latest.tar.xz
OUT.jsonl    one record per relevant package (see README "Inventory record")
SRPM_SIZES   optional "name size" lines from the rawhide source repo; marks
             packages missing from rawhide and records download size

Specs are untrusted input: they are only read as text, nothing is expanded.
A summary is printed to stdout.
"""
import collections
import json
import os
import re
import sys

# Sections that end the preamble/previous section. Shell sections are the ones
# where a verification command can actually run.
SECTION = re.compile(r'^%(prep|conf|generate_buildrequires|build|install|check|clean|'
                     r'description|package|files|changelog|pre|post|preun|postun|'
                     r'pretrans|posttrans|preuntrans|postuntrans|verify|'
                     r'trigger\w*|filetrigger\w*|transfiletrigger\w*|'
                     r'sourcelist|patchlist)\b')
SHELL_SECTIONS = {'prep', 'conf', 'generate_buildrequires', 'build', 'install', 'check'}
COND_OPEN = re.compile(r'^%(if|ifarch|ifnarch|ifos|ifnos)\b')
COND_ELSE = re.compile(r'^%(else|elif|elifarch|elifos)\b')
COND_END = re.compile(r'^%endif\b')
DEFINE = re.compile(r'^%(global|define)\s')

GPGVERIFY = re.compile(r'%(\{\??)?gpgverify\b')
OPENPGPVERIFY = re.compile(r'%(\{\??)?openpgpverify\b')
SETUP = re.compile(r'^\s*%\{?(setup|autosetup|forgeautosetup|forgesetup|gometa|cargo_prep)\b')
# A binary used as a command: at the start of a shell command, not as an
# argument (ln -s .../gpgv2, --with-gpg=.../gpg2, description text).
CMD_START = r'(?:^|[;|&(`]|\b(?:if|then|do|exec|!))\s*(?:\S*/)?'
GPG_CMD = re.compile(CMD_START + r'(gpgv2?|gpg2?)(?=\s|$)')
SQV = re.compile(CMD_START + r'(sqv(?=\s)|sq\s+(?:signature\s+)?verify\b)')
DSCVERIFY = re.compile(CMD_START + r'dscverify\s')
RHEL_COND = re.compile(r'rhel|\bel\d|epel|centos', re.I)
SIG_SOURCE = re.compile(r'\.(asc|sig|sign)$', re.I)
SOURCE_TAG = re.compile(r'^Source(\d*)\s*:\s*(\S+)', re.I)
BR_TAG = re.compile(r'^BuildRequires\s*:\s*(.*)', re.I)
SIMPLE_ARG = re.compile(r"^--(keyring|signature|data)=(['\"]?)%\{?SOURCE\d+\}?\2$|^-[ksd]\d*$|^\d+$")


def logical_lines(text):
    """Yield (lineno, line) with backslash continuations joined."""
    buf, start = '', None
    for n, line in enumerate(text.splitlines(), 1):
        if start is None:
            start = n
        if line.rstrip().endswith('\\'):
            buf += line.rstrip()[:-1] + ' '
            continue
        yield start, buf + line
        buf, start = '', None
    if buf:
        yield start, buf


def call_form(line):
    m = GPGVERIFY.search(line)
    rest = line[m.end():]
    if m.group(1) == '{?':
        return 'optional'
    if m.group(1) == '{':
        return 'braced'
    # %gpgverify without braces only works with the parametric short options;
    # with long options rpm fails with "Unknown option -".
    return 'short' if re.match(r'\s+-[ksd](\s|\d)', rest) else 'unbraced-long'


def classify(name, text):
    body = re.split(r'(?m)^%changelog\b', text, maxsplit=1)[0]
    section = 'preamble'
    conds = []              # stack of condition texts of enclosing %if blocks
    seen_setup = False
    r = dict(package=name, calls=[], openpgpverify_calls=0, raw_verify=[],
             sequoia_native=False, dscverify=False, gpg_other=[],
             br=dict(gpgverify=False, gnupg2=False, gpgv2_path=False,
                     macro=False, openpgpverify=False),
             sig_sources=[], has_check=False,
             mentions_rhel=bool(RHEL_COND.search(body) and re.search(r'%\{\?(rhel|el\d+)\}', body)),
             autochangelog=bool(re.search(r'(?m)^%autochangelog\b', text)),
             autorelease=bool(re.search(r'(?m)^Release:\s*%\{?\??autorelease', text)))
    br_conds = []
    for n, raw in logical_lines(body):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if COND_OPEN.match(line):
            conds.append(line)
            continue
        if COND_ELSE.match(line):
            if conds:
                conds[-1] += ' | ' + line
            continue
        if COND_END.match(line):
            if conds:
                conds.pop()
            continue
        m = SECTION.match(line)
        if m:
            section = m.group(1)
            if section == 'check':
                r['has_check'] = True
            continue
        if DEFINE.match(line):
            continue

        if section in ('preamble', 'package'):
            m = SOURCE_TAG.match(line)
            if m:
                fname = m.group(2).split('#/')[-1].rsplit('/', 1)[-1]
                if SIG_SOURCE.search(fname):
                    r['sig_sources'].append('Source%s' % m.group(1))
            m = BR_TAG.match(line)
            if m:
                v = m.group(1)
                hit = False
                if re.search(r'(?<![\w-])gpgverify\b', v) and not GPGVERIFY.search(v):
                    r['br']['gpgverify'] = hit = True
                if re.search(r'(?<![\w-])gnupg2?\b', v):
                    r['br']['gnupg2'] = hit = True
                if re.search(r'/gpgv2?\b', v):
                    r['br']['gpgv2_path'] = hit = True
                if GPGVERIFY.search(v):
                    r['br']['macro'] = hit = True
                if re.search(r'(?<![\w-])openpgpverify\b', v):
                    r['br']['openpgpverify'] = True
                if hit:
                    br_conds.extend(conds)
            continue
        if section not in SHELL_SECTIONS:
            continue

        if section == 'prep' and SETUP.match(line):
            seen_setup = True
        if OPENPGPVERIFY.search(line):
            r['openpgpverify_calls'] += 1
        if GPGVERIFY.search(line):
            form = call_form(line)
            args = line[GPGVERIFY.search(line).end():].lstrip('}').strip()
            stdin = '|' in line[:GPGVERIFY.search(line).start()] or '--data=-' in line
            r['calls'].append(dict(
                line=n, section=section, form=form, args=args[:300],
                stdin=stdin, after_setup=seen_setup and section == 'prep',
                conditions=list(conds),
                simple=(section == 'prep' and not stdin and not conds
                        and not (seen_setup and section == 'prep')
                        and form in ('braced', 'short')
                        and all(SIMPLE_ARG.match(a) for a in args.split()))))
            continue
        if SQV.search(line):
            r['sequoia_native'] = True
            continue
        if DSCVERIFY.search(line):
            r['dscverify'] = True
            continue
        m = GPG_CMD.search(line)
        if m:
            entry = dict(line=n, section=section, text=line[:200], conditions=list(conds))
            if m.group(1).startswith('gpgv') or '--verify' in line:
                r['raw_verify'].append(entry)
            else:
                r['gpg_other'].append(entry)

    # Conditional / RHEL-relevant: around a verification call or its BR.
    call_conds = [c for x in r['calls'] for c in x['conditions']] + \
                 [c for x in r['raw_verify'] for c in x['conditions']]
    r['conditional'] = bool(call_conds)
    r['rhel_conditional'] = any(RHEL_COND.search(c) for c in call_conds + br_conds)
    r['forms'] = sorted({c['form'] for c in r['calls']})

    # Whether gnupg2 can be dropped together with gpgverify (see README).
    if not r['br']['gnupg2']:
        r['gnupg2_action'] = None
    elif r['gpg_other'] or r['raw_verify']:
        r['gnupg2_action'] = 'keep'
    elif r['has_check']:
        r['gnupg2_action'] = 'review'
    else:
        r['gnupg2_action'] = 'remove'

    if r['openpgpverify_calls']:
        cat = 'converted'
    elif r['calls']:
        cat = 'macro-simple' if all(c['simple'] for c in r['calls']) and not r['raw_verify'] else 'macro-complex'
    elif r['raw_verify']:
        cat = 'raw-verify'
    elif r['sequoia_native']:
        cat = 'sequoia-native'
    elif r['dscverify']:
        cat = 'dscverify'
    elif r['sig_sources']:
        cat = 'sig-unverified'
    elif r['br']['gnupg2'] or r['br']['gpgverify']:
        cat = 'gnupg2-br-only'
    else:
        return None
    r['category'] = cat
    r['in_scope'] = cat in ('macro-simple', 'macro-complex', 'raw-verify')
    return r


def main():
    specdir, out = sys.argv[1], sys.argv[2]
    sizes = {}
    if len(sys.argv) > 3:
        sizes = dict(l.split() for l in open(sys.argv[3]) if l.strip())
    recs = []
    for f in sorted(os.listdir(specdir)):
        if not f.endswith('.spec'):
            continue
        with open(os.path.join(specdir, f), errors='replace') as fh:
            r = classify(f[:-5], fh.read())
        if r is None:
            continue
        if sizes:
            r['in_rawhide'] = r['package'] in sizes
            r['srpm_size'] = int(sizes.get(r['package'], 0))
        recs.append(r)
    with open(out, 'w') as fh:
        for r in recs:
            fh.write(json.dumps(r, sort_keys=True) + '\n')

    C = collections.Counter
    print('category:')
    for k, v in C(r['category'] for r in recs).most_common():
        print('  %5d  %s' % (v, k))
    scope = [r for r in recs if r['in_scope']]
    print('in scope: %d' % len(scope))
    stats = [
        ('conditional (verify inside %if)', lambda r: r['conditional']),
        ('rhel/epel conditional near verify', lambda r: r['rhel_conditional']),
        ('spec mentions %{?rhel}', lambda r: r['mentions_rhel']),
        ('optional %{?gpgverify:...}', lambda r: 'optional' in r['forms']),
        ('broken unbraced long form', lambda r: 'unbraced-long' in r['forms']),
        ('multiple calls', lambda r: len(r['calls']) > 1),
        ('stdin / pipe', lambda r: any(c['stdin'] for c in r['calls'])),
        ('after %setup', lambda r: any(c['after_setup'] for c in r['calls'])),
        ('outside %prep', lambda r: any(c['section'] != 'prep' for c in r['calls'] + r['raw_verify'])),
        ('macro + raw gpg verify', lambda r: r['calls'] and r['raw_verify']),
        ('BR gpgverify', lambda r: r['br']['gpgverify']),
        ('BR gnupg2', lambda r: r['br']['gnupg2']),
        ('BR via path/macro', lambda r: r['br']['gpgv2_path'] or r['br']['macro']),
        ('no gpg BR at all (implicit)', lambda r: not any(r['br'][k] for k in ('gpgverify', 'gnupg2', 'gpgv2_path', 'macro'))),
        ('%autochangelog', lambda r: r['autochangelog']),
        ('needs manual changelog', lambda r: not r['autochangelog']),
    ]
    for label, f in stats:
        print('  %5d  %s' % (sum(1 for r in scope if f(r)), label))
    print('  gnupg2_action: %s' % dict(C(r['gnupg2_action'] for r in scope)))
    if sizes:
        missing = [r['package'] for r in scope if not r['in_rawhide']]
        print('  not in rawhide srpm repo: %s' % (missing or 'none'))
        print('  download size: %.1f GB' % (sum(r['srpm_size'] for r in scope) / 1e9))


if __name__ == '__main__':
    main()
