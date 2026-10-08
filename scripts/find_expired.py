#!/usr/bin/python3 -I
"""Find signatures made by keys that have expired since, without full Phase 1.

Usage: find_expired.py [--jobs N] [--out FILE.jsonl] [PKG...]

Default packages: the in-scope packages that use the macro. For each:
  1. shallow clone of rawhide dist-git into work/PKG/dist-git (no sources)
  2. download only signature files (*.asc, *.sig, *.sign) from the lookaside
     cache, as listed in the `sources` file, into work/PKG/sigs/
  3. every committed file that sq reads as a keyring is inspected; each
     signature's issuer is matched to a key and its effective expiry (the
     earlier of primary key and subkey expiry) is compared with the
     signature creation time and with now

Classes per signature:
  expired-after-signing  key expired since, the signature was made while valid
  stale-keyring          the key had expired (per our copy) before signing
  valid                  the key has not expired
  no-key                 no key in the keyrings matches the issuer

Reads everything as data; no spec code is run.
"""
import argparse
import concurrent.futures
import datetime
import json
import os
import re
import subprocess
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import phase1  # noqa: E402
import state  # noqa: E402

LOOKASIDE = 'https://src.fedoraproject.org/repo/pkgs/rpms/%s/%s/%s/%s/%s'
SIG_NAME = re.compile(r'\.(asc|sig|sign)$')
NOW = datetime.datetime.now(datetime.timezone.utc)


def ts(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S').replace(
        tzinfo=datetime.timezone.utc)


def sh(cmd, timeout=120, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, **kw)


def clone(pkg, g):
    if os.path.isdir(os.path.join(g, '.git')):
        return True
    os.makedirs(os.path.dirname(g), exist_ok=True)
    return sh(['git', 'clone', '-q', '--depth', '1', '--branch', 'rawhide',
               phase1.DISTGIT % pkg, g], timeout=600).returncode == 0


def fetch_sigs(pkg, g, d):
    """Download only the signature files listed in `sources`."""
    out = []
    path = os.path.join(g, 'sources')
    if not os.path.exists(path):
        return out
    os.makedirs(d, exist_ok=True)
    for line in open(path):
        m = re.match(r'^(\w+) \((.+)\) = (\w+)$', line.strip())
        if m:
            algo, name, h = m.group(1).lower(), m.group(2), m.group(3)
        else:
            m = re.match(r'^(\w{32})\s+(\S+)$', line.strip())
            if not m:
                continue
            algo, name, h = 'md5', m.group(2), m.group(1)
        if not SIG_NAME.search(name) or '/' in name:
            continue
        dst = os.path.join(d, name)
        if not os.path.exists(dst):
            try:
                with urllib.request.urlopen(LOOKASIDE % (pkg, name, algo, h, name),
                                            timeout=60) as r:
                    data = r.read(1024 * 1024)   # signatures are small
                open(dst, 'wb').write(data)
            except Exception:
                continue
        out.append(dst)
    return out


def key_expiries(keyring):
    """{fingerprint: effective expiry or None} for every key in the keyring."""
    p = sh(['sq', 'inspect', keyring])
    res, primary_exp, cur = {}, None, None
    for line in p.stdout.splitlines():
        m = re.match(r'^\s*(Fingerprint|Subkey): ([0-9A-F]{40,64})$', line)
        if m:
            cur = m.group(2)
            if m.group(1) == 'Fingerprint':
                primary_exp = None
                res[cur] = None
            else:
                res[cur] = primary_exp
            primary = m.group(1) == 'Fingerprint'
            continue
        m = re.match(r'^\s*Expiration time: (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) UTC', line)
        if m and cur:
            e = ts(m.group(1))
            if primary:
                primary_exp = e
                res[cur] = e
            else:
                res[cur] = min(e, primary_exp) if primary_exp else e
    return res


def sig_info(path):
    p = sh(['sq', 'packet', 'dump', path])
    times = [ts(t) for t in re.findall(r'Signature creation time: (\S+ \S+) UTC', p.stdout)]
    issuers = re.findall(r'Issuer Fingerprint: ([0-9A-F]+)', p.stdout)
    issuers += [k for k in re.findall(r'Issuer: ([0-9A-F]{16})\b', p.stdout)]
    return (times[0] if times else None), issuers


def scan(pkg):
    d = os.path.join(phase1.WORK, pkg)
    g = os.path.join(d, 'dist-git')
    if not clone(pkg, g):
        return dict(package=pkg, error='clone failed')
    keys = {}
    for root, dirs, files in os.walk(g):
        dirs[:] = [x for x in dirs if x != '.git']
        for f in files:
            p = os.path.join(root, f)
            if f.endswith(('.spec', '.patch', '.diff')) or os.path.getsize(p) > 2 * 1024 * 1024:
                continue
            if re.search(r'^\s*\d+\.\s+[0-9A-F]{40}', sh(['sq', 'keyring', 'list', p]).stdout, re.M):
                for fpr, exp in key_expiries(p).items():
                    keys[fpr] = (exp, os.path.relpath(p, g))
    sigs = fetch_sigs(pkg, g, os.path.join(d, 'sigs'))
    names = {os.path.basename(x) for x in sigs}
    sigs += [os.path.join(g, f) for f in sorted(os.listdir(g))
             if SIG_NAME.search(f) and f not in names]
    results = []
    for s in sigs:
        t, issuers = sig_info(s)
        match = None
        for i in issuers:
            for fpr, (exp, kr) in keys.items():
                if fpr == i or fpr.endswith(i):
                    match = (fpr, exp, kr)
                    break
            if match:
                break
        r = dict(signature=os.path.basename(s), signed=t.isoformat() if t else None)
        if not match:
            r['class'] = 'no-key'
        else:
            fpr, exp, kr = match
            r.update(key=fpr, keyring=kr, expires=exp.isoformat() if exp else None)
            if exp is None or exp > NOW:
                r['class'] = 'valid'
            elif t and t < exp:
                r['class'] = 'expired-after-signing'
            else:
                r['class'] = 'stale-keyring'
        results.append(r)
    return dict(package=pkg, keyrings=sorted({v[1] for v in keys.values()}), signatures=results)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jobs', type=int, default=8)
    ap.add_argument('--out', default=os.path.join(state.ROOT, 'data', 'expiry-scan.jsonl'))
    ap.add_argument('packages', nargs='*')
    a = ap.parse_args()
    pkgs = a.packages or sorted(p for p, r in state.load().items()
                                if r.get('category') in ('macro-simple', 'macro-complex'))
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex, open(a.out, 'w') as fh:
        for r in ex.map(scan, pkgs):
            fh.write(json.dumps(r, sort_keys=True) + '\n')
            fh.flush()
            classes = sorted({s['class'] for s in r.get('signatures', [])})
            if 'expired-after-signing' in classes or 'stale-keyring' in classes:
                print('%-28s %s' % (r['package'], ', '.join(classes)), flush=True)


if __name__ == '__main__':
    main()
