#!/usr/bin/python3 -I
"""Propose refreshed keyrings for Phase 1 regressions, for manual review.

Usage:
  refresh_keys.py propose [PKG...]      default: regressions with a refreshable reason
  refresh_keys.py show PKG              print the review summary
  refresh_keys.py approve PKG [--note TEXT]
  refresh_keys.py reject PKG --note TEXT

A stale keyring in dist-git (the upstream key's expiry was extended, or its
self-signatures were re-made with a modern hash) is the most common reason
for openpgpverify to reject what gpgverify accepted. For each keyring used
by a failing call this:

  1. lists the certificate fingerprints already in the keyring,
  2. looks up exactly those fingerprints (`sq network search`: keyservers and
     WKD) and keeps only certificates with the same fingerprints,
  3. merges the result into the existing certificates (a merge can only add
     self-signatures, subkeys and revocations made by the same primary key),
  4. checks that the set of certificates did not change, keeps the original
     armored/binary format, and re-runs sqv on the host,
  5. writes work/PKG/refresh/FILE and work/PKG/refresh/REVIEW.md.

Nothing is used until a human approves it. Approved refreshes are applied to
the new variant by phase1.py and go into the PR.
"""
import argparse
import getpass
import hashlib
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import phase1  # noqa: E402
import state  # noqa: E402

REFRESHABLE = {'expired', 'sha1-cert', 'binding-after-signature', 'policy', 'unknown'}
FLOOD_LIMIT = 256 * 1024     # bytes; larger certificates need a closer look


def sh(cmd, timeout=180):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def fingerprints(path):
    p = sh(['sq', 'keyring', 'list', path])
    return re.findall(r'^\s*\d+\.\s+([0-9A-F]{40,64})\b', p.stdout, re.M)


def summary(path):
    """The lines of `sq inspect` that matter for review, plus the dates of the
    self-signatures (a refresh can add newer ones, or older ones our copy lacks)."""
    p = sh(['sq', 'inspect', path])
    keep = re.compile(r'Fingerprint:|Subkey:|UserID:|Expiration time:|Invalid:|because:|'
                      r'Revoked|Key flags:')
    lines = [l.rstrip() for l in (p.stdout + p.stderr).splitlines() if keep.search(l)]
    dump = sh(['sq', 'packet', 'dump', path]).stdout
    primaries = set(re.findall(r'^\s*Fingerprint: ([0-9A-F]{40,64})$', p.stdout, re.M))
    selfsig, third = {}, {}
    for chunk in re.split(r'(?m)^(?=\S.*Packet)', dump):
        if not chunk.startswith('Signature Packet'):
            continue
        t = re.search(r'^\s*Type: (\w+)', chunk, re.M)
        d = re.search(r'Signature creation time: (\S+)', chunk)
        iss = re.findall(r'Issuer(?: Fingerprint)?: ([0-9A-F]+)', chunk)
        if not (t and d):
            continue
        own = any(i == f or f.endswith(i) for i in iss for f in primaries)
        (selfsig if own else third).setdefault(t.group(1), set()).add(d.group(1))
    lines += ['self-signatures %s: %s' % (t, ', '.join(sorted(d)))
              for t, d in sorted(selfsig.items())]
    lines += ['third-party %s: %d' % (t, len(d)) for t, d in sorted(third.items())]
    return lines


def call_files(call):
    """Keyrings, signature and data paths of one logged call."""
    toks = call['args'].split()
    keyrings, sig, data, in_list = [], None, None, False
    for t in toks:
        if t.startswith('-'):
            in_list = False
        if t == '--keyrings':
            in_list = True
        elif t.startswith('--keyring='):
            keyrings.append(t.split('=', 1)[1])
        elif t.startswith('--signature='):
            sig = t.split('=', 1)[1]
        elif t.startswith('--data='):
            data = t.split('=', 1)[1]
        elif in_list:
            keyrings.append(t)
    return keyrings, sig, data


def refresh_file(src, dst, tmp):
    """Refresh one keyring file. Returns a dict describing the result."""
    fprs = fingerprints(src)
    info = dict(fingerprints=fprs, changed=False, found_via=[], size_old=os.path.getsize(src))
    if not fprs:
        info['error'] = 'no certificates found in keyring (keybox or malformed?)'
        return info
    fetched = []
    for fpr in fprs:
        raw = os.path.join(tmp, fpr + '.search.pgp')
        p = sh(['sq', '--home=none', '--batch', 'network', 'search', '--output', raw, fpr],
               timeout=300)
        info['found_via'] += sorted(set(re.findall(r'found via: (.*)', p.stdout + p.stderr)))
        if not os.path.exists(raw):
            continue
        # Keep only the certificate we asked for, never anything else: split
        # the result into one file per certificate and pick the exact match.
        parts = os.path.join(tmp, 'parts-' + fpr)
        os.makedirs(parts)
        sh(['sq', 'keyring', 'split', '--prefix', os.path.join(parts, 'c-'), raw])
        for f in sorted(os.listdir(parts)):
            if fingerprints(os.path.join(parts, f)) == [fpr]:
                fetched.append(os.path.join(parts, f))
                break
    if not fetched:
        info['error'] = 'no updates found on keyservers/WKD'
        return info
    merged = os.path.join(tmp, 'merged.pgp')
    p = sh(['sq', '--home=none', 'keyring', 'merge', '--output', merged, src] + fetched)
    if p.returncode or sorted(fingerprints(merged)) != sorted(fprs):
        info['error'] = 'merge failed or changed the set of certificates'
        return info
    armored = open(src, 'rb').read(64).lstrip().startswith(b'-----BEGIN PGP')
    if armored:
        shutil.copy(merged, dst)
    elif sh(['sq', 'packet', 'dearmor', '--output', dst, merged]).returncode:
        info['error'] = 'dearmor failed'
        return info
    info['size_new'] = os.path.getsize(dst)
    # The approval is bound to exactly this file (checked by phase1.py).
    info['sha256_new'] = hashlib.sha256(open(dst, 'rb').read()).hexdigest()
    info['changed'] = summary(src) != summary(dst)
    if info['size_new'] > FLOOD_LIMIT:
        info['warning'] = 'refreshed keyring is %d bytes (flooded third-party signatures?)' \
            % info['size_new']
    return info


def propose(pkg, rec):
    res = (rec.get('results') or [{}])[0]
    bad = [c for c in res.get('new_calls', []) if c['rc'] != 0]
    if not bad:
        return dict(status='not-applicable', note='no failing openpgpverify call')
    d = os.path.join(phase1.WORK, pkg)
    g = os.path.join(d, 'dist-git')
    out = os.path.join(d, 'refresh')
    tmp = os.path.join(out, '.tmp')
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(tmp)
    keyrings, sig, data = call_files(bad[0])
    files = []
    review = ['# Keyring refresh for %s' % pkg, '',
              'Failing call: `%s`' % bad[0]['args'], '',
              'Phase 1 reason: `%s`' % res.get('failure_reason'), '']
    for k in keyrings:
        src = phase1.host_path(k, g)
        if not src or not os.path.isfile(src):
            files.append(dict(file=k, error='keyring not in dist-git (extracted from a tarball?)'))
            continue
        rel = os.path.relpath(src, g)
        info = refresh_file(src, os.path.join(out, rel), tmp)
        info['file'] = rel
        files.append(info)
        review += ['## %s' % rel, '',
                   '- certificates: %s' % ', '.join(info['fingerprints']),
                   '- found via: %s' % ('; '.join(info['found_via']) or '-'),
                   '- size: %s → %s bytes' % (info['size_old'], info.get('size_new', '-'))]
        for key in ('error', 'warning'):
            if info.get(key):
                review.append('- **%s: %s**' % (key, info[key]))
        if info.get('size_new'):
            new = os.path.join(out, rel)
            old_s, new_s = os.path.join(tmp, 'old.summary'), os.path.join(tmp, 'new.summary')
            open(old_s, 'w').write('\n'.join(summary(src)) + '\n')
            open(new_s, 'w').write('\n'.join(summary(new)) + '\n')
            p = sh(['diff', '-u', '--label', 'dist-git/' + rel, '--label', 'refreshed/' + rel,
                    old_s, new_s], timeout=60)
            review += ['', '```diff', p.stdout.rstrip() or '(no change in sq inspect summary)',
                       '```']
        review.append('')
    changed = [f for f in files if f.get('changed')]
    # Re-run sqv on the host with the refreshed keyrings (data only, no spec code).
    host_rc = None
    sig_h, data_h = phase1.host_path(sig or '', g), phase1.host_path(data or '', g)
    if changed and sig_h and data_h and os.path.isfile(sig_h) and os.path.isfile(data_h):
        rings = [os.path.join(out, f['file']) if f.get('changed') else os.path.join(g, f['file'])
                 for f in files if 'fingerprints' in f]
        cmd = ['sqv'] + ['--keyring=' + r for r in rings] + ['--signature-file', sig_h, data_h]
        p = sh(cmd, timeout=600)
        host_rc = p.returncode
        review += ['## Verification with the refreshed keyring', '',
                   '```', '$ sqv ... %s' % os.path.basename(data_h),
                   (p.stdout + p.stderr).strip(), 'rc=%d' % host_rc, '```', '']
    elif changed:
        review += ['Host verification skipped (data from stdin or a generated file); '
                   'run phase1.py after approval.', '']
    shutil.rmtree(tmp, ignore_errors=True)
    if not changed:
        status = 'not-found' if any(f.get('error') for f in files) else 'no-update'
    elif host_rc not in (None, 0):
        status = 'still-fails'
    else:
        status = 'proposed'
    review.insert(2, '**Status: %s**' % status)
    review.insert(3, '')
    text = '\n'.join(review) + '\n'
    open(os.path.join(out, 'REVIEW.md'), 'w').write(text)
    # A copy in git, so that reviews are visible to others.
    shared = os.path.join(state.ROOT, 'reports', 'keyring-refresh')
    os.makedirs(shared, exist_ok=True)
    open(os.path.join(shared, pkg + '.md'), 'w').write(text)
    return dict(status=status, files=files, host_verify_rc=host_rc,
                review=os.path.relpath(os.path.join(out, 'REVIEW.md'), state.ROOT),
                proposed=state.now())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('action', choices=['propose', 'show', 'approve', 'reject'])
    ap.add_argument('packages', nargs='*')
    ap.add_argument('--note', default=None)
    a = ap.parse_args()
    st = state.load()
    if a.action == 'propose':
        pkgs = a.packages or sorted(
            p for p, r in st.items() if r.get('status') == 'regression' and
            (r.get('results') or [{}])[0].get('failure_reason') in REFRESHABLE)
        for pkg in pkgs:
            kr = propose(pkg, st[pkg])
            with phase1.LOCK:
                cur = state.load()
                cur[pkg]['keyring_refresh'] = kr
                cur[pkg]['updated'] = state.now()
                state.save(cur)
            print('%-28s %s' % (pkg, kr['status']), flush=True)
        return 0
    if len(a.packages) != 1:
        ap.error('%s takes exactly one package' % a.action)
    pkg = a.packages[0]
    kr = st.get(pkg, {}).get('keyring_refresh')
    if not kr:
        print('%s: no keyring refresh proposed' % pkg)
        return 1
    if a.action == 'show':
        print(open(os.path.join(state.ROOT, kr['review'])).read())
        return 0
    if a.action == 'approve' and kr['status'] != 'proposed':
        print('%s: status is %s, only "proposed" can be approved' % (pkg, kr['status']))
        return 1
    if a.action == 'reject' and not a.note:
        ap.error('reject needs --note')
    kr.update(status='approved' if a.action == 'approve' else 'rejected',
              reviewed_by=getpass.getuser(), reviewed=state.now(), review_note=a.note)
    st[pkg]['updated'] = state.now()
    state.save(st)
    print('%s: %s' % (pkg, kr['status']))
    if a.action == 'approve':
        print('re-run: scripts/phase1.py %s' % pkg)
    return 0


if __name__ == '__main__':
    sys.exit(main())
