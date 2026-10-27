#!/usr/bin/python3 -I
"""Phase 1: run %prep with gpgverify and with openpgpverify in mock.

Usage: phase1.py [--chroot CFG] [--eln] [--jobs N] [--keep] [--inventory INV] PKG...

For each package:
  1. clone rawhide dist-git (anonymous) into work/PKG/dist-git, fedpkg sources
  2. re-classify the current spec and convert it (scripts/convert.py)
  3. in a fresh mock chroot without network:
       installdeps(new) -> rpmbuild -bp new spec
       installdeps(old) -> rpmbuild -bp old spec
     with the verifier tools replaced by wrappers that log every call and its
     exit code to /tmp/opv-calls.log
  4. compare: every old call must pass, new must make the same number of
     calls (at least one), none of them through gpgverify, and all must pass
  5. diagnose regressions (keyring format, armor blocks, sq inspect)
  6. record the outcome in data/state/packages.jsonl

Nothing is pushed anywhere. Specs and sources are untrusted: they are only
parsed and executed inside mock; on the host they are read as data.
"""
import argparse
import concurrent.futures
import time
import hashlib
import json
import os
import queue
import re
import shlex
import shutil
import subprocess
import sys
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import classify  # noqa: E402
import convert  # noqa: E402
import state  # noqa: E402

HARNESS_VERSION = '5'
# Specs without %autochangelog get a Release bump and a changelog entry, done by
# rpmdev-bumpspec inside the chroot (it evaluates the spec), before %prep runs,
# so the tested spec is exactly the proposed one.
AUTHOR = 'Jakub Jelen <jjelen@redhat.com>'
CHANGELOG_LINE = 'Verify upstream source signatures with openpgpverify'
WORK = os.path.join(state.ROOT, 'work')
DISTGIT = 'https://src.fedoraproject.org/rpms/%s.git'
LOCK = threading.Lock()
GNUPG2_CHECK = True
FULL_BUILD_MAX_MB = 40   # larger sources: no full build (disk/time), BR gnupg2 stays

# Wrapped inside the chroot. Raw tools only for raw-verify packages, since
# gpgverify itself runs gpgv and would be counted twice.
MACRO_TOOLS = ['/usr/libexec/gpgverify', '/usr/libexec/openpgpverify']
RAW_TOOLS = ['/usr/bin/gpgv2', '/usr/bin/gpgv', '/usr/bin/gpg2', '/usr/bin/gpg']

WRAP_SCRIPT = r'''
set -e
mkdir -p /usr/libexec/opv-real
touch /tmp/opv-calls.log; chmod 666 /tmp/opv-calls.log
for f in %s; do
    [ -e "$f" ] || continue
    grep -q OPV-WRAPPER "$f" 2>/dev/null && continue
    real=/usr/libexec/opv-real/$(basename "$f")
    mv "$f" "$real"
    cat > "$f" <<EOF
#!/bin/bash
# OPV-WRAPPER: log the call and its exit code, then behave like the real tool
"$real" "\$@"; rc=\$?
printf '%%s\t%%s\t%%s\t%%s\n' "$(basename "$f")" "\$rc" "\$PWD" "\$*" >> /tmp/opv-calls.log
exit \$rc
EOF
    chmod 755 "$f"
done
'''

# Each variant gets its own copy of the dist-git tree (/builddir/old, /builddir/new)
# so that e.g. a refreshed keyring only affects the new run.
PREP = ('cd /builddir/%(v)s && rpmbuild %(stage)s --nodeps '
        '--define "_sourcedir /builddir/%(v)s" --define "_topdir /builddir/top-%(v)s" '
        '%(spec)s > /builddir/%(v)s.log 2>&1; echo "rpmbuild-rc: $?" >> /builddir/%(v)s.log; '
        'cp /tmp/opv-calls.log /builddir/%(v)s.calls; : > /tmp/opv-calls.log')

# gnupg2 check: when "BR: gnupg2" is dropped, prove the package does not need
# gpg. gnupg2 is in every buildroot through rpm-sign-libs, so a normal build
# proves nothing; remove it (and gpgverify) from the chroot, then build the
# changed spec completely, %check included. Tests often skip silently without
# gpg, so the build log and the unpacked test files are searched for gpg too.
GNUPG2_REMOVE = (
    "rpm -qa --qf '%{NAME}\\n' 'gnupg2*' gpgverify sequoia-chameleon-gnupg "
    "> /builddir/gpg-removed.txt; xargs -r rpm -e --nodeps < /builddir/gpg-removed.txt; "
    "for t in gpg gpg2 gpgv gpgv2 gpgconf gpg-agent gpgsm; do command -v $t; done "
    "> /builddir/gpg-left.txt; true")
GPG_WORD = r'\b(gpg|gpg2|gpgv|gpgv2|gpgconf|gpgsm|gpg-agent)\b|GNUPGHOME|gnupg'
GNUPG2_TREE = (
    "cd /builddir/top-new/BUILD 2>/dev/null && grep -rIlE '%s' . 2>/dev/null "
    "| grep -E '(^|/)(t|tests?|testing|testsuite|testdata)/|(^|/)test_|_test\\.|\\.t$' "
    "| head -20 | xargs -r -d '\\n' grep -nHE '%s' | cut -c1-200 | head -40 "
    "> /builddir/gpg-tree.txt; true" % (GPG_WORD, GPG_WORD))
# %generate_buildrequires: "mock --installdeps SPEC" only knows the static
# BuildRequires; resolve the dynamic ones like mock does, before gnupg2 goes.
# rpmbuild -br exits with 11 while some of them are missing.
DYN_BR = ('cd /builddir/new && rm -rf /builddir/top-new/SRPMS && rpmbuild -br '
          '--define "_sourcedir /builddir/new" --define "_topdir /builddir/top-new" '
          '%(spec)s > /builddir/dynbr.log 2>&1; [ $? = 11 ] && '
          'cp /builddir/top-new/SRPMS/*.buildreqs.nosrc.rpm /builddir/dynbr.nosrc.rpm; '
          ': > /tmp/opv-calls.log')
# Each full build starts from a pristine copy of the new tree: %prep may move
# or delete files in the source directory (grout moves a tarball away).
FULL_BUILD = ('rm -rf /builddir/full /builddir/top-full && cp -a /builddir/new.orig /builddir/full '
              '&& cd /builddir/full && timeout %(timeout)d rpmbuild -bb --nodeps '
              '--define "_sourcedir /builddir/full" --define "_topdir /builddir/top-full" '
              '%(spec)s > /builddir/%(log)s 2>&1; echo "rpmbuild-rc: $?" >> /builddir/%(log)s')
FULL_BUILD_TIMEOUT = 2 * 3600
# gpg named as a command in the build log (keyring file names like gpgkey-*.gpg
# and the openpgpverify call itself do not count)
LOG_GPG = re.compile(r'(?<![\w./-])(gpg2?|gpgv2?|gpgconf|gpgsm|gpg-agent)(?![\w.-])|GNUPGHOME|gnupg',
                     re.I)

ENV_INFO = ('rpm -q rpm openpgpverify gpgverify sequoia-sqv gnupg2; '
            'echo "crypto-policy: $(cat /etc/crypto-policies/config 2>/dev/null)"; '
            'echo "SEQUOIA_CRYPTO_POLICY=${SEQUOIA_CRYPTO_POLICY:-unset}"')


def run(cmd, log, timeout=3600, **kw):
    with open(log, 'a') as fh:
        fh.write('$ %s\n' % ' '.join(shlex.quote(c) for c in cmd))
        fh.flush()
        p = subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT,
                           timeout=timeout, cwd=WORK, **kw)
    return p.returncode


class Mock:
    # One mock root per parallel job ("slot"), reused across packages: the
    # bootstrap and caches stay, the build chroot is scrubbed after each package.
    def __init__(self, cfg, slot, log):
        self.base = ['mock', '-r', cfg, '--uniqueext', slot, '--quiet']
        self.log = log

    def __call__(self, *args, timeout=3600):
        return run(self.base + list(args), self.log, timeout=timeout)

    def chroot(self, script, unpriv=False):
        return self('--unpriv', '--chroot', script) if unpriv else self('--chroot', script)


def checkout(pkg, d, log):
    os.makedirs(d, exist_ok=True)
    g = os.path.join(d, 'dist-git')
    if os.path.isdir(os.path.join(g, '.git')):
        rc = run(['git', '-C', g, 'fetch', '--depth', '1', 'origin', 'rawhide'], log) or \
             run(['git', '-C', g, 'reset', '--hard', 'FETCH_HEAD'], log)
    else:
        rc = run(['git', 'clone', '--depth', '1', '--branch', 'rawhide', DISTGIT % pkg, g], log)
    if rc:
        return None, 'git clone/fetch failed'
    if os.path.exists(os.path.join(g, 'dead.package')):
        return None, 'retired (dead.package)'
    if run(['fedpkg', '--path', g, '--name', pkg, 'sources'], log, timeout=7200):
        return None, 'fedpkg sources failed'
    return g, None


def read_calls(path):
    calls = []
    if os.path.exists(path):
        for line in open(path, errors='replace'):
            tool, rc, cwd, args = (line.rstrip('\n').split('\t', 3) + ['', '', ''])[:4]
            calls.append(dict(tool=tool, rc=int(rc or -1), cwd=cwd, args=args[:400]))
    return calls


def prep_rc(log):
    m = re.search(r'^rpmbuild-rc: (\d+)', open(log, errors='replace').read(), re.M) \
        if os.path.exists(log) else None
    return int(m.group(1)) if m else None


def tail(path, n=25):
    if not os.path.exists(path):
        return ''
    return ''.join(open(path, errors='replace').readlines()[-n:])[-3000:]


def host_path(path, g, overlay=None):
    """Map a /builddir/{old,new}/FILE path from the chroot to the host file."""
    m = re.match(r'^/builddir/(old|new)/(.+)$', path.strip('\'"'))
    if not m:
        return None
    if m.group(1) == 'new' and overlay and m.group(2) in overlay:
        return overlay[m.group(2)]
    return os.path.join(g, m.group(2))


def diagnose(call, g, overlay=None):
    """Look at keyring and signature files of a failed call (on the host, as data)."""
    d = {}
    opts = dict(re.findall(r'--(keyring|signature|data)=(\S+)', call['args']))
    for kind in ('keyring', 'signature'):
        host = host_path(opts.get(kind, ''), g, overlay)
        if not host:
            continue
        if not os.path.isfile(host):
            continue
        data = open(host, 'rb').read()
        if kind == 'keyring':
            d['keyring_format'] = ('keybox' if data[8:12] == b'KBXf' else
                                   'armored' if b'-----BEGIN PGP PUBLIC KEY BLOCK' in data else
                                   'binary')
            p = subprocess.run(['sq', 'inspect', host], capture_output=True, text=True, timeout=60)
            d['keyring_inspect'] = (p.stdout + p.stderr)[-1500:]
        else:
            d['armor_blocks'] = data.count(b'-----BEGIN PGP SIGNATURE-----')
            p = subprocess.run(['sq', 'packet', 'dump', host], capture_output=True, text=True,
                               timeout=60)
            algos = sorted(set(re.findall(r'Hash algo: (\S+)', p.stdout)))
            d['sig_hash_algos'] = algos
    return d


def failure_reason(diag, text):
    t = text.lower()
    if 'malformed certificate in keyring' in t or 'unknown version' in t:
        return 'unparseable-cert'  # e.g. old v3 keys in an Apache KEYS file
    if diag.get('keyring_format') == 'keybox':
        return 'keybox'
    if diag.get('armor_blocks', 0) > 1:
        return 'concatenated-armor'
    if 'packet v3' in t:
        return 'v3-sig'            # ancient signature format; upstream must re-sign
    if re.search(r'(dsa\d+|rsa1024|elgamal\d+) is not considered secure', t):
        return 'weak-key'          # key algorithm rejected; upstream needs a new key
    if 'SHA1' in diag.get('sig_hash_algos', []):
        return 'sha1-sig'          # upstream must re-sign the release
    if 'sha1' in t:
        return 'sha1-cert'         # key bindings use SHA-1; a refreshed key may fix it
    if 'expired' in t:
        return 'expired'
    if 'no binding signature at time' in t:
        return 'binding-after-signature'   # keyring lacks older self-signatures; refresh
    if 'not considered secure' in t or 'policy' in t:
        return 'policy'
    return 'unknown'


def installdeps_srpm(m, spec, g, out, v):
    """Fallback: some specs need their sources to be parsed (e.g. "%load
    %{SOURCE10}"), which --installdeps on a spec can't provide. Build an SRPM
    with the sources and install its BuildRequires instead."""
    rd = os.path.join(out, 'srpm-' + v)
    os.makedirs(rd, exist_ok=True)
    if m('--buildsrpm', '--spec', spec, '--sources', g, '--no-clean', '--no-cleanup-after',
         '--resultdir', rd, timeout=3600):
        return False
    srpms = [f for f in os.listdir(rd) if f.endswith('.src.rpm')]
    ok = bool(srpms) and m('--installdeps', os.path.join(rd, srpms[0]), timeout=7200) == 0
    shutil.rmtree(rd, ignore_errors=True)   # an SRPM holds all sources again
    return ok


def gnupg2_verdict(res, out, has_check):
    """Decide from the gnupg2 check whether "BR: gnupg2" can go."""
    def lines(f):
        f = os.path.join(out, f)
        return [l.strip() for l in open(f, errors='replace')] if os.path.exists(f) else []
    left = [l for l in lines('gpg-left.txt') if l]
    tree = [l for l in lines('gpg-tree.txt') if l]
    log_hits = [l[:200] for l in lines('new-build.log')
                if LOG_GPG.search(l) and 'openpgpverify' not in l][:20]
    chk = dict(has_check=has_check, gpg_left=left, tree_hits=tree, log_hits=log_hits,
               build_rc=prep_rc(os.path.join(out, 'new-build.log'))
               if os.path.exists(os.path.join(out, 'new-build.log')) else None,
               baseline_rc=prep_rc(os.path.join(out, 'base-build.log'))
               if os.path.exists(os.path.join(out, 'base-build.log')) else None)
    if left:
        chk.update(verdict='keep', reason='gpg still installed after removing gnupg2: %s' % left)
    elif res.get('new_prep_rc') != 0:
        if res.get('new_calls') and all(c['rc'] == 0 for c in res['new_calls']):
            reason = ('not checked: the signature check passes, but `rpmbuild %s` fails '
                      'later, with the unchanged spec too' % res.get('stage', '-bp')
                      if res.get('old_prep_rc') else
                      'not checked: `rpmbuild` fails after the signature check')
        else:
            reason = 'not checked: the changed spec does not get past the signature check'
        chk.update(verdict='keep', reason=reason)
    elif chk['build_rc'] != 0:
        if any('No space left on device' in l for f in ('new-build.log', 'base-build.log')
               for l in lines(f)):
            reason = 'not checked: the build ran out of disk space on the test machine'
        elif chk['baseline_rc'] == 0:
            reason = 'the build fails without gnupg2 and passes with it'
        elif log_hits:
            reason = 'the build fails without gnupg2 and its log shows gpg use (%s)' % log_hits[0]
        elif chk['build_rc'] == 124:
            reason = 'not checked: the build did not finish in %d h' % (FULL_BUILD_TIMEOUT // 3600)
        else:
            reason = 'not checked: the build fails with gnupg2 too (rc %s)' % chk['baseline_rc']
        chk.update(verdict='keep', reason=reason)
    elif log_hits or tree and has_check:   # tests that never run don't matter
        chk.update(verdict='keep', reason='the build log or test files mention gpg; tests may '
                   'skip without it')
    else:
        chk.update(verdict='drop', reason='full build including %check passed without gnupg2 '
                   'installed; no gpg use in the build log or test files')
    return chk


def test_in_chroot(cfg, pkg, d, g, old_spec, new_spec, raw, stage='-bp', overlay=None,
                   bump=False, slot='opv-0', gnupg2_check=False, has_check=False,
                   dynamic_br=False):
    """Run old and new %prep in one fresh chroot. Returns a result dict."""
    log = os.path.join(d, 'mock-%s.log' % cfg)
    open(log, 'w').close()
    out = os.path.join(d, 'out-' + cfg)
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    m = Mock(cfg, slot, log)
    res = dict(chroot=cfg, stage=stage)
    wrap = WRAP_SCRIPT % ' '.join(MACRO_TOOLS + (RAW_TOOLS if raw else []))
    try:
        if m('--clean') or m('--init', timeout=3600):
            res['error'] = 'mock init failed'
            return res
        def populate():
            """(Re)create /builddir/old and /builddir/new; mock --buildsrpm wipes them."""
            m.chroot('rm -rf /builddir/old /builddir/new')
            copies = [m('--copyin', g, '/builddir/old')]
            if new_spec:
                copies.append(m('--copyin', g, '/builddir/new'))
                copies.append(m('--copyin', new_spec, '/builddir/new/%s.spec' % pkg))
                for rel, src in (overlay or {}).items():
                    copies.append(m('--copyin', src, '/builddir/new/' + rel))
            return not any(copies) and not m.chroot(
                'chown -R mockbuild:mock /builddir/old' + (' /builddir/new' if new_spec else ''))

        if not populate():
            res['error'] = 'copyin failed'
            return res
        variants = ([('new', new_spec)] if new_spec else []) + [('old', old_spec)]
        if gnupg2_check:
            # gnupg2 is removed before the new run, so the old one goes first
            variants.reverse()
        for v, spec in variants:
            if m('--installdeps', spec, timeout=7200):
                if not installdeps_srpm(m, spec, g, out, v) or not populate():
                    res['%s_error' % v] = 'installdeps failed'
                    continue
                res.setdefault('notes', []).append('%s: build deps installed from SRPM' % v)
            if v == 'new' and bump:
                if m('--install', 'rpmdevtools') or m.chroot(
                        'rpmdev-bumpspec -u %s -c %s /builddir/new/%s.spec'
                        % (shlex.quote(AUTHOR), shlex.quote(CHANGELOG_LINE), pkg),
                        unpriv=True):
                    res['new_error'] = 'rpmdev-bumpspec failed'
                    continue
                m('--copyout', '/builddir/new/%s.spec' % pkg, os.path.join(out, 'bumped.spec'))
            if v == 'new' and gnupg2_check:
                m.chroot('rm -rf /builddir/new.orig && cp -a /builddir/new /builddir/new.orig',
                         unpriv=True)
            m.chroot(wrap)
            # After the new variant's deps, so sequoia-sqv is installed
            if v == 'new' or not new_spec:
                m.chroot('{ %s; } > /builddir/env.txt 2>&1' % ENV_INFO)
                m('--copyout', '/builddir/env.txt', out)
            if v == 'new' and gnupg2_check and dynamic_br:
                for _ in range(5):
                    if os.path.exists(os.path.join(out, 'dynbr.nosrc.rpm')):
                        os.remove(os.path.join(out, 'dynbr.nosrc.rpm'))
                    m.chroot(DYN_BR % dict(spec='%s.spec' % pkg), unpriv=True)
                    m('--copyout', '/builddir/dynbr.nosrc.rpm', out)
                    nosrc = os.path.join(out, 'dynbr.nosrc.rpm')
                    if not os.path.exists(nosrc):
                        break     # all dynamic BuildRequires are installed
                    m('--installdeps', nosrc, timeout=7200)
                    m.chroot('rm -f /builddir/dynbr.nosrc.rpm')
            if v == 'new' and gnupg2_check:
                m.chroot(GNUPG2_REMOVE)
                m('--copyout', '/builddir/gpg-left.txt', out)
                m('--copyout', '/builddir/gpg-removed.txt', out)
            m.chroot(PREP % dict(v=v, spec='%s.spec' % pkg, stage=stage), unpriv=True)
            for f in ('%s.log' % v, '%s.calls' % v):
                m('--copyout', '/builddir/' + f, out)
            res['%s_calls' % v] = read_calls(os.path.join(out, '%s.calls' % v))
            res['%s_prep_rc' % v] = prep_rc(os.path.join(out, '%s.log' % v))
            if v == 'new' and gnupg2_check and res['new_prep_rc'] == 0 and \
                    not open(os.path.join(out, 'gpg-left.txt')).read().strip():
                m.chroot(GNUPG2_TREE, unpriv=True)
                m('--copyout', '/builddir/gpg-tree.txt', out)
                full = dict(spec='%s.spec' % pkg, timeout=FULL_BUILD_TIMEOUT)
                m.chroot(FULL_BUILD % dict(full, log='new-build.log'), unpriv=True)
                m('--copyout', '/builddir/new-build.log', out)
                if prep_rc(os.path.join(out, 'new-build.log')) not in (0, 124):
                    # pre-existing FTBFS, or does it need gpg?
                    m('--install', *(open(os.path.join(out, 'gpg-removed.txt')).read().split()
                                     or ['gnupg2']))
                    m.chroot(FULL_BUILD % dict(full, log='base-build.log'), unpriv=True)
                    m('--copyout', '/builddir/base-build.log', out)
        if gnupg2_check:
            res['gnupg2_check'] = gnupg2_verdict(res, out, has_check)
    finally:
        if not KEEP:
            m('--scrub', 'chroot')
    env = os.path.join(out, 'env.txt')
    if os.path.exists(env):
        t = open(env).read()
        res['env'] = dict(re.findall(r'^(sequoia-sqv|openpgpverify|gpgverify|rpm)-(\S+)', t, re.M))
        mp = re.search(r'crypto-policy: (\S*)', t)
        res['crypto_policy'] = mp.group(1) if mp else None
    return res


def evaluate(res, raw, g, primary=True, rewritten=None):
    """Turn the call logs of one chroot run into an outcome."""
    if 'error' in res:
        return 'error', res['error']
    old = res.get('old_calls', [])
    if raw and not rewritten:
        # Only the baseline can be run; the rewrite is manual.
        if not old:
            return 'manual', 'raw verification: no gpg call executed in baseline'
        return 'manual', 'raw verification baseline %s' % (
            'passes' if all(c['rc'] == 0 for c in old) else 'FAILS')
    new = res.get('new_calls', [])
    if res.get('old_error'):
        return 'not-buildable', 'unchanged spec: %s' % res['old_error']
    if res.get('new_error'):
        return 'error', res.get('new_error') or res.get('old_error')
    if not old:
        if not primary:
            # e.g. verification inside "%if 0%{?fedora}": nothing to compare in ELN
            return 'not-verified', 'the unchanged spec does not verify sources in this chroot'
        return 'guard-failed', 'old spec executed no gpgverify call (prep rc %s)' % res.get('old_prep_rc')
    if not rewritten and any(c['tool'] != 'gpgverify' for c in old):
        return 'guard-failed', 'unexpected tools in old run: %s' % sorted({c['tool'] for c in old})
    if any(c['tool'] != 'openpgpverify' for c in new):
        return 'guard-failed', 'new spec still runs %s' % sorted(
            {c['tool'] for c in new} - {'openpgpverify'})
    if any(c['rc'] != 0 for c in old):
        return 'both-fail', 'old verification fails already (rc %s)' % [c['rc'] for c in old]
    if rewritten:
        # gpg calls (key import, verify) don't map 1:1 onto openpgpverify calls
        if not new:
            return 'guard-failed', 'new spec executed no openpgpverify call'
    elif len(new) != len(old):
        # a failing call stops %prep, so fewer new calls are fine if the last one failed
        if not (new and new[-1]['rc'] != 0 and len(new) < len(old)):
            return 'guard-failed', 'old ran %d verify calls, new ran %d' % (len(old), len(new))
    bad = [c for c in new if c['rc'] != 0]
    if bad:
        return 'regression', None
    return 'both-pass', None


def test_package(pkg, inv_rec, cfgs, prev=None, slot='opv-0'):
    d = os.path.join(WORK, pkg)
    os.makedirs(d, exist_ok=True)
    log = os.path.join(d, 'checkout.log')
    open(log, 'w').close()
    upd = dict(harness_version=HARNESS_VERSION, results=[], outcome_detail=None,
               release_bumped=False, tested_at=state.now())
    g, err = checkout(pkg, d, log)
    if not g:
        upd.update(status='skipped' if 'retired' in err else 'error', outcome_detail=err)
        return upd
    spec_path = os.path.join(g, pkg + '.spec')
    text = open(spec_path, errors='replace').read()
    upd['spec_commit'] = subprocess.run(['git', '-C', g, 'rev-parse', 'HEAD'],
                                        capture_output=True, text=True).stdout.strip()
    upd['spec_sha256'] = hashlib.sha256(text.encode()).hexdigest()
    rec = classify.classify(pkg, text)
    if rec is None or rec['category'] == 'converted':
        upd.update(status='superseded', outcome_detail='already converted or no longer verifying')
        return upd
    if not rec['in_scope']:
        upd.update(status='skipped', outcome_detail='now %s' % rec['category'])
        return upd
    # What the current spec does, not what the inventory snapshot said.
    upd.update(autochangelog=rec['autochangelog'], autorelease=rec['autorelease'],
               rhel_conditional=rec['rhel_conditional'], gnupg2_action=rec['gnupg2_action'])
    raw = bool(rec['raw_verify'])
    new_spec = None
    # Direct gpg/gpgv calls: rewrite them into %{gpgverify} calls (simple
    # gpgv form automatically, anything else by a hand-written
    # manual/PKG.patch), then convert like any other spec. The raw tools stay
    # wrapped in both runs, so a leftover gpg call in the new spec shows up.
    rewritten = None
    src_text = text
    if raw:
        try:
            mp = convert.manual_patch(pkg)
            if mp:
                pr = subprocess.run(['patch', '-s', '--no-backup-if-mismatch', '-o', '-',
                                     spec_path, mp], capture_output=True, text=True)
                if pr.returncode:
                    raise convert.Unconvertible('%s does not apply to the current spec'
                                                % os.path.relpath(mp, state.ROOT))
                src_text, rewritten = pr.stdout, 'manual'
            else:
                src_text, rewritten = convert.rewrite_raw(text, rec), 'auto'
            rec2 = classify.classify(pkg, src_text)
            if not rec2 or not rec2['calls'] or \
                    any(not convert.non_fedora(x) for x in rec2['raw_verify']):
                raise convert.Unconvertible('the rewrite left direct gpg calls')
            rec = dict(rec2, raw_verify=[])   # only old-EL branches keep gpgv
            upd.update(rhel_conditional=rec['rhel_conditional'],
                       gnupg2_action=rec['gnupg2_action'])
        except convert.Unconvertible as e:
            upd['convert_notes'] = ['unconvertible: %s' % e]
            rewritten, src_text = None, text
    upd['raw_rewritten'] = rewritten
    # Drop "BR: gnupg2" whenever the spec has no other gpg use, and prove it
    # with the gnupg2 check; the variant keeping it is the fallback.
    gnupg2_check = GNUPG2_CHECK and (not raw or rewritten) and \
        rec['gnupg2_action'] in ('remove', 'review')
    too_big = ((inv_rec or {}).get('srpm_size') or 0) > FULL_BUILD_MAX_MB * 1e6
    if gnupg2_check and too_big:
        gnupg2_check = False
        upd['gnupg2_check'] = dict(verdict='keep', has_check=rec['has_check'],
                                   reason='not checked: sources over %d MB, too large for '
                                   'the full build without gnupg2 on the test machine'
                                   % FULL_BUILD_MAX_MB)
    keep_text = None
    if not raw or rewritten:
        try:
            # None (legacy, --no-gnupg2-check): drop only without %check
            new_text, notes = convert.convert(
                src_text, rec, drop_gnupg2=gnupg2_check if GNUPG2_CHECK else None)
            if gnupg2_check:
                keep_text, _ = convert.convert(src_text, rec, drop_gnupg2=False)
                open(os.path.join(d, pkg + '.opv-unbumped.spec'), 'w').write(new_text)
            new_spec = os.path.join(d, pkg + '.opv.spec')
            open(new_spec, 'w').write(new_text)
            upd['convert_notes'] = notes
            subprocess.run(['diff', '-u', spec_path, new_spec], stdout=open(
                os.path.join(d, 'conversion.diff'), 'w'))
        except convert.Unconvertible as e:
            upd['convert_notes'] = ['unconvertible: %s' % e]
            raw, rewritten = True, None   # run the baseline only
            new_spec = None
    # Verification outside %prep (e.g. at the start of %build) needs a later stage;
    # failures after the verify call do not matter, the wrapper has logged it.
    # Approved keyring refreshes (scripts/refresh_keys.py) replace keyring files
    # in the new variant only.
    overlay = None
    upd['keyring_refresh_applied'] = []
    kr = (prev or {}).get('keyring_refresh') or {}
    if new_spec and kr.get('status') == 'approved':
        overlay = {f['file']: os.path.join(d, 'refresh', f['file'])
                   for f in kr['files'] if f.get('changed')}
        for f in kr['files']:
            if f.get('changed') and hashlib.sha256(open(overlay[f['file']], 'rb').read()) \
                    .hexdigest() != f.get('sha256_new'):
                upd.update(status='error', outcome_detail='approved keyring %s changed after '
                           'review; propose and review again' % f['file'])
                return upd
        upd['keyring_refresh_applied'] = sorted(overlay)
        # Record how the keyring was refreshed in the spec, next to its Source.
        text = open(new_spec).read()
        for f in kr['files']:
            if f.get('changed') and f.get('spec_commands'):
                text, note = convert.refresh_comment(text, pkg, os.path.basename(f['file']),
                                                     f['spec_commands'])
                if note:
                    upd.setdefault('convert_notes', []).append(note)
        with open(new_spec, 'w') as fh:
            fh.write(text)
        subprocess.run(['diff', '-u', spec_path, new_spec], stdout=open(
            os.path.join(d, 'conversion.diff'), 'w'))
    sections = {c['section'] for c in rec['calls'] + rec['raw_verify']}
    stage = '-bp' if sections <= {'prep'} else '-bc' if sections <= {'prep', 'conf', 'build'} else '-bi'
    upd['stage'] = stage
    statuses = []
    for cfg in cfgs:
        res = test_in_chroot(cfg, pkg, d, g, spec_path, new_spec, raw, stage, overlay,
                             bump=bool(new_spec) and not rec['autochangelog']
                             and not rec['autorelease'], slot=slot,
                             gnupg2_check=gnupg2_check and cfg == cfgs[0],
                             has_check=rec['has_check'],
                             dynamic_br='%generate_buildrequires' in text)
        bumped = os.path.join(d, 'out-' + cfg, 'bumped.spec')
        if cfg == cfgs[0] and os.path.exists(bumped):
            shutil.copy(bumped, new_spec)
            upd['release_bumped'] = True
            subprocess.run(['diff', '-u', spec_path, new_spec], stdout=open(
                os.path.join(d, 'conversion.diff'), 'w'))
        outcome, detail = evaluate(res, raw, g, primary=(cfg == cfgs[0]), rewritten=rewritten)
        res['outcome'] = outcome
        res['detail'] = detail
        if outcome == 'regression':
            bad = [c for c in res['new_calls'] if c['rc'] != 0][0]
            text_tail = tail(os.path.join(d, 'out-' + cfg, 'new.log'))
            diag = diagnose(bad, g, overlay)
            res['diag'] = diag
            res['failure_reason'] = failure_reason(diag, text_tail)
            res['log_tail'] = text_tail
        elif outcome in ('both-fail', 'guard-failed', 'error'):
            res['log_tail'] = tail(os.path.join(d, 'out-' + cfg, 'old.log')) or tail(
                os.path.join(d, 'mock-%s.log' % cfg))
        upd['results'].append(res)
        statuses.append(outcome)
        if 'gnupg2_check' in res:
            upd['gnupg2_check'] = res['gnupg2_check']
    if gnupg2_check and new_spec:
        chk = upd.get('gnupg2_check') or dict(verdict='keep', reason='check did not run')
        upd['gnupg2_check'] = chk
        if chk['verdict'] != 'drop':
            # same spec with "BR: gnupg2" kept: apply the Release bump to it
            keep_spec = os.path.join(d, pkg + '.opv-keep.spec')
            open(keep_spec, 'w').write(keep_text)
            bump = subprocess.run(['diff', '-u', os.path.join(d, pkg + '.opv-unbumped.spec'),
                                   new_spec], capture_output=True, text=True).stdout
            if bump and subprocess.run(['patch', '-s', '--no-backup-if-mismatch', keep_spec],
                                       input=bump, text=True, capture_output=True).returncode:
                upd.update(status='error', outcome_detail='cannot apply the Release bump '
                           'to the spec keeping gnupg2')
                return upd
            shutil.move(keep_spec, new_spec)
            subprocess.run(['diff', '-u', spec_path, new_spec], stdout=open(
                os.path.join(d, 'conversion.diff'), 'w'))
    # The first chroot (rawhide) decides; extra chroots (ELN) count only if they
    # could test the unchanged spec at all.
    order = ['error', 'guard-failed', 'regression', 'both-fail', 'not-buildable', 'manual',
             'not-verified', 'both-pass']
    statuses = statuses[:1] + [x for x in statuses[1:]
                               if x not in ('not-buildable', 'not-verified')]
    worst = min(statuses, key=order.index)
    upd['status'] = {'both-pass': 'tested'}.get(worst, worst)
    upd['outcome_detail'] = '; '.join('%s: %s%s' % (r['chroot'], r['outcome'],
                                      ' (%s)' % r['detail'] if r['detail'] else '')
                                      for r in upd['results'])
    first = upd['results'][0]
    upd['expanded_calls_old'] = len(first.get('old_calls', []))
    upd['expanded_calls_new'] = len(first.get('new_calls', []))
    upd['sqv_version'] = first.get('env', {}).get('sequoia-sqv')
    upd['crypto_policy'] = first.get('crypto_policy')
    return upd


def main():
    global KEEP, GNUPG2_CHECK, FULL_BUILD_MAX_MB
    ap = argparse.ArgumentParser()
    ap.add_argument('--chroot', default='fedora-rawhide-x86_64')
    ap.add_argument('--eln', action='store_true',
                    help='also test in fedora-eln-x86_64 when the spec has rhel conditionals')
    ap.add_argument('--jobs', type=int, default=1)
    ap.add_argument('--keep', action='store_true', help='keep mock chroots for debugging')
    ap.add_argument('--full-build-max-mb', type=float, default=FULL_BUILD_MAX_MB)
    ap.add_argument('--no-gnupg2-check', action='store_true',
                    help='keep "BR: gnupg2" in specs with %%check instead of proving with a '
                         'full build that it can go')
    ap.add_argument('--min-free-gb', type=float, default=1.5,
                    help='do not start a package with less free disk than this')
    ap.add_argument('--size-factor', type=float, default=12,
                    help='also require SIZE_FACTOR x the source RPM size free (unpacking)')
    ap.add_argument('--stop-after-min', type=float, default=None,
                    help='start no new package after this many minutes')
    ap.add_argument('--prune-sources', action='store_true',
                    help='delete downloaded sources of packages that passed (saves disk); '
                         'failing ones keep them for refresh_keys.py')
    ap.add_argument('--inventory', default=os.path.join(
        state.ROOT, 'data/inventory/inventory-2026-10-06.jsonl'))
    ap.add_argument('packages', nargs='+')
    a = ap.parse_args()
    KEEP = a.keep
    GNUPG2_CHECK = not a.no_gnupg2_check
    FULL_BUILD_MAX_MB = a.full_build_max_mb
    inv = state.load_inventory(a.inventory)
    os.makedirs(WORK, exist_ok=True)

    started = time.time()
    done_count = [0]
    skipped = []
    slots = queue.Queue()
    for i in range(a.jobs):
        slots.put('opv-%d' % i)

    def one(pkg):
        if a.stop_after_min and time.time() - started > a.stop_after_min * 60:
            skipped.append((pkg, 'time limit'))
            return
        need = max(a.min_free_gb * 1e9,
                   a.size_factor * (inv.get(pkg, {}).get('srpm_size') or 0))
        # Space is freed when the other job finishes its package: wait for it,
        # but don't wait for space that won't come (more than the disk can give).
        waited = 0
        while shutil.disk_usage(WORK).free < need and waited < 900 and \
                need < shutil.disk_usage(WORK).total * 0.25:
            time.sleep(15)
            waited += 15
        free = shutil.disk_usage(WORK).free
        if free < need:
            skipped.append((pkg, 'disk: %.1f GB free, needs %.1f GB' % (free / 1e9, need / 1e9)))
            print('%-28s %-13s %s' % (pkg, 'not-started', skipped[-1][1]), flush=True)
            return
        cfgs = [a.chroot]
        if a.eln and inv.get(pkg, {}).get('mentions_rhel'):
            cfgs.append('fedora-eln-x86_64')
        try:
            with LOCK:
                prev = state.load().get(pkg)
            slot = slots.get()
            try:
                upd = test_package(pkg, inv.get(pkg), cfgs, prev, slot)
            finally:
                slots.put(slot)
        except Exception as e:  # keep going with other packages
            upd = dict(status='error', outcome_detail='harness: %r' % e, results=[])
        with LOCK:
            done_count[0] += 1
            scrub_cache = done_count[0] % 20 == 0
        if scrub_cache:
            # mock keeps every downloaded package; on a small disk that adds up
            for cfg in {a.chroot, 'fedora-eln-x86_64'}:
                for i in range(a.jobs):
                    subprocess.run(['mock', '-r', cfg, '--uniqueext', 'opv-%d' % i, '--quiet',
                                    '--scrub=dnf-cache'], capture_output=True, cwd=WORK)
        g = os.path.join(WORK, pkg, 'dist-git')
        # Failing packages are pruned too; refresh_keys.py downloads the
        # sources again if it needs them.
        if a.prune_sources and os.path.isdir(os.path.join(g, '.git')):
            subprocess.run(['git', '-C', g, 'clean', '-fdxq'])
        upd['updated'] = state.now()
        with LOCK:
            st = state.load()
            st.setdefault(pkg, dict(package=pkg)).update(upd)
            state.save(st)
        print('%-28s %-13s %s' % (pkg, upd['status'], upd.get('outcome_detail') or ''), flush=True)

    with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
        list(ex.map(one, a.packages))
    if skipped:
        print('not started: %d (%s)' % (len(skipped), ', '.join(
            sorted({why.split(':')[0] for _, why in skipped}))), flush=True)


KEEP = False
if __name__ == '__main__':
    main()
