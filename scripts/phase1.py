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
import hashlib
import json
import os
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

HARNESS_VERSION = '3'
# Specs without %autochangelog get a Release bump and a changelog entry, done by
# rpmdev-bumpspec inside the chroot (it evaluates the spec), before %prep runs,
# so the tested spec is exactly the proposed one.
AUTHOR = 'Jakub Jelen <jjelen@redhat.com>'
CHANGELOG_LINE = 'Verify upstream source signatures with openpgpverify'
WORK = os.path.join(state.ROOT, 'work')
DISTGIT = 'https://src.fedoraproject.org/rpms/%s.git'
LOCK = threading.Lock()

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
    def __init__(self, cfg, pkg, log):
        self.base = ['mock', '-r', cfg, '--uniqueext', 'opv-' + pkg, '--quiet']
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
    if diag.get('keyring_format') == 'keybox':
        return 'keybox'
    if diag.get('armor_blocks', 0) > 1:
        return 'concatenated-armor'
    if 'packet v3' in t:
        return 'v3-sig'            # ancient signature format; upstream must re-sign
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


def test_in_chroot(cfg, pkg, d, g, old_spec, new_spec, raw, stage='-bp', overlay=None,
                   bump=False):
    """Run old and new %prep in one fresh chroot. Returns a result dict."""
    log = os.path.join(d, 'mock-%s.log' % cfg)
    open(log, 'w').close()
    out = os.path.join(d, 'out-' + cfg)
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(out)
    m = Mock(cfg, pkg, log)
    res = dict(chroot=cfg)
    wrap = WRAP_SCRIPT % ' '.join(MACRO_TOOLS + (RAW_TOOLS if raw else []))
    try:
        if m('--clean') or m('--init', timeout=3600):
            res['error'] = 'mock init failed'
            return res
        copies = [m('--copyin', g, '/builddir/old')]
        if new_spec:
            copies.append(m('--copyin', g, '/builddir/new'))
            copies.append(m('--copyin', new_spec, '/builddir/new/%s.spec' % pkg))
            for rel, src in (overlay or {}).items():
                copies.append(m('--copyin', src, '/builddir/new/' + rel))
        if any(copies) or m.chroot('chown -R mockbuild:mock /builddir/old /builddir/new'
                                   if new_spec else 'chown -R mockbuild:mock /builddir/old'):
            res['error'] = 'copyin failed'
            return res
        variants = ([('new', new_spec)] if new_spec else []) + [('old', old_spec)]
        for v, spec in variants:
            if m('--installdeps', spec, timeout=7200):
                res['%s_error' % v] = 'installdeps failed'
                continue
            if v == 'new' and bump:
                if m('--install', 'rpmdevtools') or m.chroot(
                        'rpmdev-bumpspec -u %s -c %s /builddir/new/%s.spec'
                        % (shlex.quote(AUTHOR), shlex.quote(CHANGELOG_LINE), pkg),
                        unpriv=True):
                    res['new_error'] = 'rpmdev-bumpspec failed'
                    continue
                m('--copyout', '/builddir/new/%s.spec' % pkg, os.path.join(out, 'bumped.spec'))
            m.chroot(wrap)
            if v == variants[0][0]:
                m.chroot('{ %s; } > /builddir/env.txt 2>&1' % ENV_INFO)
                m('--copyout', '/builddir/env.txt', out)
            m.chroot(PREP % dict(v=v, spec='%s.spec' % pkg, stage=stage), unpriv=True)
            for f in ('%s.log' % v, '%s.calls' % v):
                m('--copyout', '/builddir/' + f, out)
            res['%s_calls' % v] = read_calls(os.path.join(out, '%s.calls' % v))
            res['%s_prep_rc' % v] = prep_rc(os.path.join(out, '%s.log' % v))
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


def evaluate(res, raw, g):
    """Turn the call logs of one chroot run into an outcome."""
    if 'error' in res:
        return 'error', res['error']
    old = res.get('old_calls', [])
    if raw:
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
        return 'guard-failed', 'old spec executed no gpgverify call (prep rc %s)' % res.get('old_prep_rc')
    if any(c['tool'] != 'gpgverify' for c in old):
        return 'guard-failed', 'unexpected tools in old run: %s' % sorted({c['tool'] for c in old})
    if any(c['tool'] != 'openpgpverify' for c in new):
        return 'guard-failed', 'new spec still runs gpgverify'
    if any(c['rc'] != 0 for c in old):
        return 'both-fail', 'gpgverify fails already (rc %s)' % [c['rc'] for c in old]
    if len(new) != len(old):
        # a failing call stops %prep, so fewer new calls are fine if the last one failed
        if not (new and new[-1]['rc'] != 0 and len(new) < len(old)):
            return 'guard-failed', 'old ran %d verify calls, new ran %d' % (len(old), len(new))
    bad = [c for c in new if c['rc'] != 0]
    if bad:
        return 'regression', None
    return 'both-pass', None


def test_package(pkg, inv_rec, cfgs, prev=None):
    d = os.path.join(WORK, pkg)
    os.makedirs(d, exist_ok=True)
    log = os.path.join(d, 'checkout.log')
    open(log, 'w').close()
    upd = dict(harness_version=HARNESS_VERSION, results=[], outcome_detail=None,
               release_bumped=False)
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
    raw = bool(rec['raw_verify'])
    new_spec = None
    if not raw:
        try:
            new_text, notes = convert.convert(text, rec)
            new_spec = os.path.join(d, pkg + '.opv.spec')
            open(new_spec, 'w').write(new_text)
            upd['convert_notes'] = notes
            subprocess.run(['diff', '-u', spec_path, new_spec], stdout=open(
                os.path.join(d, 'conversion.diff'), 'w'))
        except convert.Unconvertible as e:
            upd['convert_notes'] = ['unconvertible: %s' % e]
            raw = True   # run the baseline only
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
    sections = {c['section'] for c in rec['calls'] + rec['raw_verify']}
    stage = '-bp' if sections <= {'prep'} else '-bc' if sections <= {'prep', 'conf', 'build'} else '-bi'
    upd['stage'] = stage
    statuses = []
    for cfg in cfgs:
        res = test_in_chroot(cfg, pkg, d, g, spec_path, new_spec, raw, stage, overlay,
                             bump=bool(new_spec) and not rec['autochangelog'])
        bumped = os.path.join(d, 'out-' + cfg, 'bumped.spec')
        if cfg == cfgs[0] and os.path.exists(bumped):
            shutil.copy(bumped, new_spec)
            upd['release_bumped'] = True
            subprocess.run(['diff', '-u', spec_path, new_spec], stdout=open(
                os.path.join(d, 'conversion.diff'), 'w'))
        outcome, detail = evaluate(res, raw, g)
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
    # The first chroot (rawhide) decides; extra chroots (ELN) count only if they
    # could test the unchanged spec at all.
    order = ['error', 'guard-failed', 'regression', 'both-fail', 'not-buildable', 'manual',
             'both-pass']
    statuses = statuses[:1] + [x for x in statuses[1:] if x != 'not-buildable']
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
    global KEEP
    ap = argparse.ArgumentParser()
    ap.add_argument('--chroot', default='fedora-rawhide-x86_64')
    ap.add_argument('--eln', action='store_true',
                    help='also test in fedora-eln-x86_64 when the spec has rhel conditionals')
    ap.add_argument('--jobs', type=int, default=1)
    ap.add_argument('--keep', action='store_true', help='keep mock chroots for debugging')
    ap.add_argument('--inventory', default=os.path.join(
        state.ROOT, 'data/inventory/inventory-2026-10-06.jsonl'))
    ap.add_argument('packages', nargs='+')
    a = ap.parse_args()
    KEEP = a.keep
    inv = state.load_inventory(a.inventory)
    os.makedirs(WORK, exist_ok=True)

    def one(pkg):
        cfgs = [a.chroot]
        if a.eln and inv.get(pkg, {}).get('mentions_rhel'):
            cfgs.append('fedora-eln-x86_64')
        try:
            with LOCK:
                prev = state.load().get(pkg)
            upd = test_package(pkg, inv.get(pkg), cfgs, prev)
        except Exception as e:  # keep going with other packages
            upd = dict(status='error', outcome_detail='harness: %r' % e, results=[])
        upd['updated'] = state.now()
        with LOCK:
            st = state.load()
            st.setdefault(pkg, dict(package=pkg)).update(upd)
            state.save(st)
        print('%-28s %-13s %s' % (pkg, upd['status'], upd.get('outcome_detail') or ''), flush=True)

    with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
        list(ex.map(one, a.packages))


KEEP = False
if __name__ == '__main__':
    main()
