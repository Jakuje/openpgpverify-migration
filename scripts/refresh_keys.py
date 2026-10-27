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
import signal
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import convert  # noqa: E402
import phase1  # noqa: E402
import state  # noqa: E402

REFRESHABLE = {'expired', 'sha1-cert', 'binding-after-signature', 'policy', 'unknown'}
FLOOD_LIMIT = 256 * 1024     # bytes; larger certificates need a closer look


def sh(cmd, timeout=180, cwd=None):
    """Run a command; on timeout kill its whole process group (fedpkg starts
    downloaders that would otherwise keep the pipes open and block forever)."""
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                         start_new_session=True, cwd=cwd)
    try:
        out, err = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        out, err = p.communicate()
        return subprocess.CompletedProcess(cmd, -9, out, err + '\ntimed out after %ds' % timeout)
    return subprocess.CompletedProcess(cmd, p.returncode, out, err)


def fingerprints(path):
    p = sh(['sq', 'keyring', 'list', path])
    # A keyring (e.g. an Apache KEYS file) may list the same key twice.
    return list(dict.fromkeys(re.findall(r'^\s*\d+\.\s+([0-9A-F]{40,64})\b', p.stdout, re.M)))


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


def is_keybox(path):
    """A GnuPG keybox ("gpg --keyring" files made by gpg >= 2.1), which gpgv
    reads but sqv does not."""
    with open(path, 'rb') as fh:
        head = fh.read(12)
    return len(head) == 12 and head[8:12] == b'KBXf'


def recipe(name, fprs, keybox, armored):
    """The shell commands that refresh keyring file NAME in the current
    directory. refresh_file() runs exactly these, and the PR and the spec
    comment quote them, so anyone can repeat the refresh."""
    cmds = []
    base = name
    if keybox:
        # gpgv reads GnuPG keyboxes, sqv does not: export to a plain keyring first.
        base = name + '.pgp'
        cmds.append('gpg --homedir "$(mktemp -d)" --batch --no-default-keyring '
                    '--keyring ./%s --export --output %s' % (name, base))
    certs = ' '.join('--cert %s' % f for f in fprs)
    cmds.append('sq --home=none network search --output - %s \\\n'
                '  | sq keyring filter --experimental %s --output update.pgp'
                % (' '.join(fprs), certs))
    if armored:
        cmds.append('sq keyring merge --output %s.new %s update.pgp' % (name, base))
    else:
        cmds.append('sq keyring merge %s update.pgp | sq packet dearmor --output %s.new'
                    % (base, name))
    cmds.append('mv %s.new %s' % (name, name))
    return cmds


def refresh_file(src, dst, tmp):
    """Refresh one keyring file by running recipe() in a scratch directory.
    Returns a dict describing the result."""
    name = os.path.basename(src)
    keybox = is_keybox(src)
    run = os.path.join(tmp, 'run-' + name)
    os.makedirs(run)
    shutil.copy(src, os.path.join(run, name))
    info = dict(fingerprints=[], changed=False, found_via=[], size_old=os.path.getsize(src),
                keybox=keybox)
    base = src
    if keybox:
        export = recipe(name, [], True, False)[0]
        if sh(['bash', '-o', 'pipefail', '-c', export], cwd=run).returncode:
            info['error'] = 'keybox export failed'
            return info
        base = os.path.join(tmp, 'from-keybox.pgp')
        shutil.copy(os.path.join(run, name + '.pgp'), base)
    fprs = fingerprints(base)
    info['fingerprints'] = fprs
    if not fprs:
        info['error'] = 'no certificates found in keyring (malformed?)'
        return info
    armored = open(src, 'rb').read(64).lstrip().startswith(b'-----BEGIN PGP')
    cmds = recipe(name, fprs, keybox, armored)
    info['commands'] = cmds
    # For the spec comment: the next refresh starts from the plain keyring.
    info['spec_commands'] = recipe(name, fprs, False, armored)
    for c in cmds[1 if keybox else 0:]:
        p = sh(['bash', '-o', 'pipefail', '-c', c], cwd=run, timeout=600)
        info['found_via'] += sorted(set(re.findall(r'found via: (.*)', p.stdout + p.stderr)))
        if p.returncode:
            if 'network search' in c and not keybox:
                info['error'] = 'no updates found on keyservers/WKD'
                return info
            if 'network search' in c:
                # Nothing newer, but the exported keyring alone may be enough.
                open(os.path.join(run, 'update.pgp'), 'wb').close()
                continue
            info['error'] = 'refresh command failed: %s: %s' % (c, (p.stderr or '').strip()[-300:])
            return info
    out = os.path.join(run, name)
    if sorted(fingerprints(out)) != sorted(fprs):
        info['error'] = 'merge changed the set of certificates'
        return info
    shutil.copy(out, dst)
    info['size_new'] = os.path.getsize(dst)
    # The approval is bound to exactly this file (checked by phase1.py).
    info['sha256_new'] = hashlib.sha256(open(dst, 'rb').read()).hexdigest()
    info['changed'] = keybox or summary(src) != summary(dst)
    if info['size_new'] > FLOOD_LIMIT:
        info['warning'] = 'refreshed keyring is %d bytes (flooded third-party signatures?)' \
            % info['size_new']
    return info


def key_urls(text, pkg, name):
    """URLs the spec gives for keyring file NAME: its Source URL and URLs in
    the comment right above that Source line. Only simple macros are expanded
    (name, version, one-word %global/%define); the spec is never evaluated."""
    macros = dict(re.findall(r'(?m)^%(?:global|define)\s+(\w+)\s+([^\s%]+)\s*$', text))
    macros['name'] = pkg
    m = re.search(r'(?mi)^Version\s*:\s*([^\s%]+)\s*$', text)
    if m:
        macros['version'] = m.group(1)

    def expand(v):
        for _ in range(3):
            v = re.sub(r'%\{\??(\w+)\}|%(\w+)\b',
                       lambda x: macros.get(x.group(1) or x.group(2), x.group(0)), v)
        return v
    lines = text.split('\n')
    for i, line in enumerate(lines):
        m = convert.SOURCE_TAG.match(line)
        if not m:
            continue
        value = expand(m.group(2))
        if value.split('#/')[-1].rsplit('/', 1)[-1] != name:
            continue
        top = i
        while top > 0 and lines[top - 1].startswith('#'):
            top -= 1
        urls = []
        for u in re.findall(r'https?://[^\s<>"\']+', expand(' '.join(lines[top:i + 1]))):
            u = u.split('#')[0].rstrip(').,;')
            if '%' not in u and u not in urls:
                urls.append(u)
        return urls
    return []


def upstream_file(src, url, dst, tmp):
    """Download URL; keep it only if it holds exactly the certificates of SRC."""
    name = os.path.basename(src)
    info = dict(url=url, size_old=os.path.getsize(src), method='upstream-url',
                commands=['curl -fsSL -o %s %s' % (name, url)])
    dl = os.path.join(tmp, 'download')
    if os.path.exists(dl):
        os.remove(dl)
    p = sh(['curl', '-fsSL', '--proto', '=https,http', '--max-time', '120',
            '--max-filesize', str(20 * 1024 * 1024), '-o', dl, url], timeout=180)
    if p.returncode or not os.path.exists(dl):
        info['error'] = 'download failed (curl rc %d)' % p.returncode
        return info
    old = src
    if is_keybox(src):
        run = os.path.join(tmp, 'kbx')
        shutil.rmtree(run, ignore_errors=True)
        os.makedirs(run)
        shutil.copy(src, os.path.join(run, name))
        sh(['bash', '-c', recipe(name, [], True, False)[0]], cwd=run)
        old = os.path.join(run, name + '.pgp')
        info['keybox'] = True
    fo, fn = fingerprints(old), fingerprints(dl)
    info['fingerprints'] = fo
    if not fn:
        info['error'] = 'no OpenPGP certificate at the URL (a web page?)'
        return info
    if sorted(fn) != sorted(fo):
        info['error'] = 'different certificates at the URL: %s' % ', '.join(
            ['+' + f for f in fn if f not in fo] + ['-' + f for f in fo if f not in fn])
        return info
    if open(dl, 'rb').read() == open(src, 'rb').read():
        info['error'] = 'the URL serves the same file as dist-git'
        return info
    shutil.copy(dl, dst)
    info['size_new'] = os.path.getsize(dst)
    info['sha256_new'] = hashlib.sha256(open(dst, 'rb').read()).hexdigest()
    info['changed'] = True
    info['old_summary_base'] = old != src
    return info


def propose_upstream(pkg, rec):
    """Like propose(), but take the keyring from the URL the spec names."""
    res = (rec.get('results') or [{}])[0]
    bad = [c for c in res.get('new_calls', []) if c['rc'] != 0]
    if not bad:
        return dict(status='not-applicable', note='no failing openpgpverify call')
    d = os.path.join(phase1.WORK, pkg)
    g = os.path.join(d, 'dist-git')
    spec = open(os.path.join(g, pkg + '.spec')).read()
    keyrings, sig, data = call_files(bad[0])
    out = os.path.join(d, 'upstream')
    tmp = os.path.join(out, '.tmp')
    shutil.rmtree(out, ignore_errors=True)
    os.makedirs(tmp)
    files, tried = [], []
    for k in keyrings:
        src = phase1.host_path(k, g)
        if not src or not os.path.isfile(src):
            continue
        rel = os.path.relpath(src, g)
        os.makedirs(os.path.dirname(os.path.join(out, rel)), exist_ok=True)
        for url in key_urls(spec, pkg, os.path.basename(rel)):
            info = upstream_file(src, url, os.path.join(out, rel), tmp)
            info['file'] = rel
            tried.append(info)
            if info.get('changed'):
                files.append(info)
                break
    if not tried:
        shutil.rmtree(out, ignore_errors=True)
        return dict(status='no-url', method='upstream-url')
    if not files:
        shutil.rmtree(tmp, ignore_errors=True)
        return dict(status='not-found', method='upstream-url',
                    tried=[dict(url=t['url'], error=t.get('error')) for t in tried])
    for f in (sig, data):
        h = phase1.host_path(f or '', g)
        if h and not os.path.exists(h):
            sh(['fedpkg', '--path', g, '--name', pkg, 'sources'], timeout=900)
            break
    host_rc = None
    sig_h, data_h = phase1.host_path(sig or '', g), phase1.host_path(data or '', g)
    review = ['# Keyring update from upstream for %s' % pkg, '',
              'Failing call: `%s`' % bad[0]['args'], '',
              'Phase 1 reason: `%s`' % res.get('failure_reason'), '']
    if sig_h and data_h and os.path.isfile(sig_h) and os.path.isfile(data_h):
        new = {f['file']: os.path.join(out, f['file']) for f in files}
        rings = [new.get(os.path.relpath(phase1.host_path(k, g), g), phase1.host_path(k, g))
                 for k in keyrings]
        p = sh(['sqv'] + ['--keyring=' + r for r in rings] +
               ['--signature-file', sig_h, data_h], timeout=600)
        host_rc = p.returncode
        verify = ['## Verification with the upstream keyring', '', '```',
                  '$ sqv ... %s' % os.path.basename(data_h), (p.stdout + p.stderr).strip(),
                  'rc=%d' % host_rc, '```', '']
    else:
        verify = ['Host verification skipped (data from stdin or a generated file); '
                  'run phase1.py after approval.', '']
    for f in files:
        rel = f['file']
        base = os.path.join(tmp, 'kbx', os.path.basename(rel) + '.pgp') \
            if f.pop('old_summary_base') else os.path.join(g, rel)
        old_s, new_s = os.path.join(tmp, 'old.summary'), os.path.join(tmp, 'new.summary')
        open(old_s, 'w').write('\n'.join(summary(base)) + '\n')
        open(new_s, 'w').write('\n'.join(summary(os.path.join(out, rel))) + '\n')
        p = sh(['diff', '-u', '--label', 'dist-git/' + rel, '--label', 'upstream/' + rel,
                old_s, new_s], timeout=60)
        review += ['## %s' % rel, '', '- from: %s' % f['url'],
                   '- certificates (unchanged): %s' % ', '.join(f['fingerprints']),
                   '- size: %s → %s bytes' % (f['size_old'], f['size_new']), '',
                   '```', *f['commands'], '```', '',
                   '```diff', p.stdout.rstrip() or '(no change in sq inspect summary)', '```', '']
    review += verify
    shutil.rmtree(tmp, ignore_errors=True)
    status = 'still-fails' if host_rc not in (None, 0) else 'proposed'
    review.insert(2, '**Status: %s**' % status)
    review.insert(3, '')
    text = '\n'.join(review) + '\n'
    open(os.path.join(out, 'REVIEW.md'), 'w').write(text)
    shared = os.path.join(state.ROOT, 'reports', 'keyring-upstream')
    os.makedirs(shared, exist_ok=True)
    open(os.path.join(shared, pkg + '.md'), 'w').write(text)
    return dict(status=status, method='upstream-url', files=files, host_verify_rc=host_rc,
                review=os.path.relpath(os.path.join(out, 'REVIEW.md'), state.ROOT),
                proposed=state.now())


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
    # Sources may have been pruned after Phase 1 (phase1.py --prune-sources).
    for f in (sig, data):
        h = phase1.host_path(f or '', g)
        if h and not os.path.exists(h):
            sh(['fedpkg', '--path', g, '--name', pkg, 'sources'], timeout=900)
            break
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
                   *(['- **format: GnuPG keybox, converted to an OpenPGP keyring '
                      '(sqv does not read keyboxes)**'] if info.get('keybox') else []),
                   '- certificates: %s' % ', '.join(info['fingerprints']),
                   '- found via: %s' % ('; '.join(info['found_via']) or '-'),
                   '- size: %s → %s bytes' % (info['size_old'], info.get('size_new', '-'))]
        if info.get('commands'):
            review += ['', 'Commands (run in a copy of dist-git):', '', '```'] + \
                info['commands'] + ['```']
        for key in ('error', 'warning'):
            if info.get(key):
                review.append('- **%s: %s**' % (key, info[key]))
        if info.get('size_new'):
            new = os.path.join(out, rel)
            old_s, new_s = os.path.join(tmp, 'old.summary'), os.path.join(tmp, 'new.summary')
            # A keybox has no readable summary; compare with its plain export.
            base = os.path.join(tmp, 'from-keybox.pgp') if info.get('keybox') else src
            open(old_s, 'w').write('\n'.join(summary(base)) + '\n')
            open(new_s, 'w').write('\n'.join(summary(new)) + '\n')
            label = 'dist-git/' + rel + (' (exported from keybox)' if info.get('keybox') else '')
            p = sh(['diff', '-u', '--label', label, '--label', 'refreshed/' + rel,
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
    ap.add_argument('action', choices=['propose', 'propose-upstream', 'show', 'approve',
                                       'reject'])
    ap.add_argument('packages', nargs='*')
    ap.add_argument('--note', default=None)
    a = ap.parse_args()
    st = state.load()
    if a.action == 'propose':
        pkgs = a.packages or sorted(
            p for p, r in st.items() if r.get('status') == 'regression' and
            (r.get('results') or [{}])[0].get('failure_reason') in REFRESHABLE)
        for pkg in pkgs:
            try:
                kr = propose(pkg, st[pkg])
            except Exception as e:  # one broken package must not stop the run
                kr = dict(status='error', note='refresh_keys: %r' % e, proposed=state.now())
            with phase1.LOCK:
                cur = state.load()
                cur[pkg]['keyring_refresh'] = kr
                cur[pkg]['updated'] = state.now()
                state.save(cur)
            print('%-28s %s' % (pkg, kr['status']), flush=True)
        return 0
    if a.action == 'propose-upstream':
        pkgs = a.packages or sorted(p for p, r in st.items() if r.get('status') == 'regression')
        for pkg in pkgs:
            try:
                up = propose_upstream(pkg, st[pkg])
            except Exception as e:  # one broken package must not stop the run
                up = dict(status='error', method='upstream-url', note='%r' % e)
            d = os.path.join(phase1.WORK, pkg)
            with phase1.LOCK:
                cur = state.load()
                r = cur[pkg]
                r['upstream_key'] = {k: v for k, v in up.items() if k != 'files'}
                if up['status'] == 'proposed':
                    # Preferred over a keyserver refresh: it is what the spec names.
                    if r.get('keyring_refresh', {}).get('method') != 'upstream-url':
                        r['keyring_refresh_keyserver'] = r.get('keyring_refresh')
                        shutil.rmtree(os.path.join(d, 'refresh-keyserver'), ignore_errors=True)
                        if os.path.isdir(os.path.join(d, 'refresh')):
                            os.rename(os.path.join(d, 'refresh'),
                                      os.path.join(d, 'refresh-keyserver'))
                    shutil.rmtree(os.path.join(d, 'refresh'), ignore_errors=True)
                    os.rename(os.path.join(d, 'upstream'), os.path.join(d, 'refresh'))
                    up['review'] = os.path.relpath(os.path.join(d, 'refresh', 'REVIEW.md'),
                                                   state.ROOT)
                    r['keyring_refresh'] = up
                r['updated'] = state.now()
                state.save(cur)
            print('%-28s %s %s' % (pkg, up['status'], '; '.join(
                '%s: %s' % (t['url'], t['error']) for t in up.get('tried', []))[:200]),
                  flush=True)
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
