#!/usr/bin/python3 -I
"""Propose refreshed keyrings for Phase 1 regressions, for manual review.

Usage:
  refresh_keys.py propose [PKG...]      default: regressions with a refreshable reason
  refresh_keys.py propose-upstream [--url URL] [PKG...]
                                        the keyring file from upstream, byte for byte
  refresh_keys.py propose-key --url URL [--keyserver] PKG...
                                        rebuild the keyring from the key at URL,
                                        completed from keyservers with --keyserver
  refresh_keys.py show PKG              print the review summary
  refresh_keys.py approve PKG [--note TEXT]
  refresh_keys.py reject PKG --note TEXT

A stale keyring in dist-git (the upstream key's expiry was extended, or its
self-signatures were re-made with a modern hash) is the most common reason
for openpgpverify to reject what gpgverify accepted. For each keyring used
by a failing call this:

  1. lists the certificate fingerprints already in the keyring,
  2. replaces the keyring with what the keyservers have for exactly those
     fingerprints (`sq network keyserver search`, armored output),
  3. checks that the set of certificates did not change, and re-runs sqv on
     the host,
  4. writes work/PKG/refresh/FILE and work/PKG/refresh/REVIEW.md.

Nothing is used until a human approves it. Approved refreshes are applied to
the new variant by phase1.py and go into the PR.
"""
import argparse
import getpass
import hashlib
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import convert  # noqa: E402
import phase1  # noqa: E402
import state  # noqa: E402

UPSTREAM_METHODS = ('upstream-url', 'key-url', 'key-url+keyserver')
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


def keybox_export(name, base):
    """Plain export of GnuPG keybox NAME, only to read its fingerprints: gpgv
    reads keyboxes, sqv does not. The new file itself comes from the keyservers."""
    return ('gpg --homedir "$(mktemp -d)" --batch --no-default-keyring '
            '--keyring ./%s --export --output %s' % (name, base))


def recipe(name, fprs):
    """The shell commands that refresh keyring file NAME in the current
    directory. refresh_file() runs exactly these, and the PR and the spec
    comment quote them, so anyone can repeat the refresh."""
    keys = fprs[0] if len(fprs) == 1 else '\\\n  ' + ' \\\n  '.join(fprs) + ' \\\n '
    return ['sq --home=none network keyserver search %s --output %s --overwrite' % (keys, name)]


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
        export = keybox_export(name, name + '.pgp')
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
    cmds = recipe(name, fprs)
    info['commands'] = cmds
    info['spec_commands'] = cmds
    for c in cmds:
        p = sh(['bash', '-o', 'pipefail', '-c', c], cwd=run, timeout=600)
        info['found_via'] += sorted(set(re.findall(r'found via: (.*)', p.stdout + p.stderr)))
        if p.returncode:
            info['error'] = 'no updates found on keyservers'
            return info
    out = os.path.join(run, name)
    # sq succeeds when only some of the keys are found.
    if sorted(fingerprints(out)) != sorted(fprs):
        info['error'] = 'keyservers returned a different set of certificates'
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


def upstream_file(src, url, dst, tmp, replace=False, superset=False):
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
        sh(['bash', '-c', keybox_export(name, name + '.pgp')], cwd=run)
        old = os.path.join(run, name + '.pgp')
        info['keybox'] = True
    fo, fn = fingerprints(old), fingerprints(dl)
    info['fingerprints'] = fo
    if not fn:
        info['error'] = 'no OpenPGP certificate at the URL (a web page?)'
        return info
    if replace and fn and not [f for f in fn if f not in fo]:
        # Asked for: the file at the URL replaces the keyring, dropping the other keys.
        info['dropped'] = [f for f in fo if f not in fn]
        info['fingerprints'] = fo = fn
    if superset and not [f for f in fo if f not in fn]:
        # Asked for: upstream's file also holds other keys of the project.
        info['added'] = [f for f in fn if f not in fo]
        fn = fo
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


def key_recipe(name, url, fprs, keyserver, keep_old, armored):
    """The commands that rebuild keyring NAME from the key published at URL:
    optionally completed from keyservers/WKD (upstream publishes only the
    current key there; the older self-signatures and subkeys a release may need
    are on the keyservers), and merged into the old keyring when the URL holds
    only some of its certificates. key_file() runs exactly these."""
    cmds = ['curl -fsSL -o key.asc %s' % url]
    parts = ['key.asc']
    if keyserver:
        cmds.append('sq --home=none network search --output - %s \\\n'
                    '  | sq keyring filter --experimental %s --output update.pgp'
                    % (' '.join(fprs), ' '.join('--cert %s' % f for f in fprs)))
        parts.append('update.pgp')
    if keep_old:
        parts.insert(0, name)
    if armored:
        cmds.append('sq keyring merge --output %s.new %s' % (name, ' '.join(parts)))
    else:
        cmds.append('sq keyring merge %s | sq packet dearmor --output %s.new'
                    % (' '.join(parts), name))
    cmds.append('mv %s.new %s' % (name, name))
    cmds.append('rm -f %s' % ' '.join(p for p in parts if p != name))
    return cmds


def key_file(src, url, dst, tmp, keyserver):
    """Rebuild one keyring file from the key at URL by running key_recipe()."""
    name = os.path.basename(src)
    info = dict(url=url, size_old=os.path.getsize(src),
                method='key-url+keyserver' if keyserver else 'key-url')
    if is_keybox(src):
        info['error'] = 'keybox in dist-git; not supported here'
        return info
    run = os.path.join(tmp, 'run-' + name)
    shutil.rmtree(run, ignore_errors=True)
    os.makedirs(run)
    dl = os.path.join(tmp, 'download')
    p = sh(['curl', '-fsSL', '--proto', '=https,http', '--max-time', '120',
            '--max-filesize', str(20 * 1024 * 1024), '-o', dl, url], timeout=180)
    if p.returncode or not os.path.exists(dl):
        info['error'] = 'download failed (curl rc %d)' % p.returncode
        return info
    fo, fu = fingerprints(src), fingerprints(dl)
    info['fingerprints'] = fo
    if not fu:
        info['error'] = 'no OpenPGP certificate at the URL (a web page?)'
        return info
    if [f for f in fu if f not in fo]:
        info['error'] = 'the URL has certificates the keyring does not: %s' % ', '.join(
            f for f in fu if f not in fo)
        return info
    keep_old = sorted(fu) != sorted(fo)
    info['url_fingerprints'] = fu
    armored = open(src, 'rb').read(64).lstrip().startswith(b'-----BEGIN PGP')
    cmds = key_recipe(name, url, fu, keyserver, keep_old, armored)
    info['commands'] = info['spec_commands'] = cmds
    info['spec_header'] = ('# Upstream signing key from %s%s:' % (
        'its website' if not keep_old else 'upstream, merged into this keyring',
        ', completed from keyservers/WKD' if keyserver else ''))
    shutil.copy(src, os.path.join(run, name))
    for c in cmds:
        p = sh(['bash', '-o', 'pipefail', '-c', c], cwd=run, timeout=600)
        info.setdefault('found_via', [])
        info['found_via'] += sorted(set(re.findall(r'found via: (.*)', p.stdout + p.stderr)))
        if p.returncode:
            info['error'] = 'command failed: %s: %s' % (c, (p.stderr or '').strip()[-300:])
            return info
    info['found_via'] = sorted({h for v in info['found_via'] for h in v.split(', ')})
    out = os.path.join(run, name)
    if sorted(fingerprints(out)) != sorted(fo):
        info['error'] = 'the result has a different set of certificates'
        return info
    if open(out, 'rb').read() == open(src, 'rb').read():
        info['error'] = 'the result is the same file as dist-git'
        return info
    shutil.copy(out, dst)
    info['size_new'] = os.path.getsize(dst)
    info['sha256_new'] = hashlib.sha256(open(dst, 'rb').read()).hexdigest()
    info['changed'] = True
    info['old_summary_base'] = False
    if info['size_new'] > FLOOD_LIMIT:
        info['warning'] = 'keyring is %d bytes (flooded third-party signatures?)' \
            % info['size_new']
    return info


def propose_upstream(pkg, rec, url=None, keyserver=None, replace=False, source_url=False,
                     superset=False):
    """Like propose(), but take the keyring from the URL the spec names, or
    from URL (e.g. one upstream pointed us to); a URL not in the spec is
    added to the comment above the keyring's Source line."""
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
    method = 'upstream-url' if keyserver is None else \
        'key-url+keyserver' if keyserver else 'key-url'
    files, tried = [], []
    for k in keyrings:
        src = phase1.host_path(k, g)
        if not src or not os.path.isfile(src):
            continue
        rel = os.path.relpath(src, g)
        os.makedirs(os.path.dirname(os.path.join(out, rel)), exist_ok=True)
        for u in [url] if url else key_urls(spec, pkg, os.path.basename(rel)):
            if keyserver is not None:
                info = key_file(src, u, os.path.join(out, rel), tmp, keyserver)
            else:
                info = upstream_file(src, u, os.path.join(out, rel), tmp, replace, superset)
            info['file'] = rel
            if source_url and keyserver is None and info.get('changed'):
                # The Source line becomes the URL; the file is named like it.
                # A "#/NAME" fragment names the file when the URL has no usable name.
                base = u.split('#/')[-1] if '#/' in u else u.rsplit('/', 1)[-1]
                new = os.path.join(os.path.dirname(rel), base)
                if new != rel and os.path.exists(os.path.join(g, new)):
                    info.update(changed=False, error='%s already exists in dist-git' % new)
                else:
                    info['source_url'] = u
                    if new != rel:
                        info['new_file'] = new
                    info['commands'] = ['curl -fsSL -o %s \'%s\'' % (base, u.split('#')[0])
                                        if '#/' in u else 'curl -fsSL -O %s' % u]
            elif keyserver is None and url and u not in key_urls(spec, pkg, os.path.basename(rel)):
                info['spec_header'] = '# Upstream signing key:'
                info['spec_commands'] = info['commands']
            tried.append(info)
            if info.get('changed'):
                files.append(info)
                break
    if not tried:
        shutil.rmtree(out, ignore_errors=True)
        return dict(status='no-url', method=method)
    if not files:
        shutil.rmtree(tmp, ignore_errors=True)
        return dict(status='not-found', method=method,
                    tried=[dict(url=t['url'], error=t.get('error')) for t in tried])
    for f in (sig, data):
        h = phase1.host_path(f or '', g)
        if h and not os.path.exists(h):
            sh(['fedpkg', '--path', g, '--name', pkg, 'sources', '--force'], timeout=900)
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
                   *(['- **renamed to `%s`; its `Source` line becomes the URL**' % f['new_file']]
                     if f.get('new_file') else []),
                   *(['- completed from keyservers/WKD, found via: %s'
                      % '; '.join(f['found_via'])] if f.get('found_via') else []),
                   *(['- merged into the existing keyring (the URL has %s only)'
                      % ', '.join(f['url_fingerprints'])]
                     if f.get('url_fingerprints') and
                     sorted(f['url_fingerprints']) != sorted(f['fingerprints']) else []),
                   *(['- **replaces the keyring: drops %s** (asked for)'
                      % ', '.join(f['dropped'])] if f.get('dropped') else []),
                   *(['- **adds keys the URL also holds: %s** (asked for)'
                      % ', '.join(f['added'])] if f.get('added') else []),
                   '- certificates%s: %s' % (' (kept)' if f.get('dropped') else ' (unchanged)',
                                             ', '.join(f['fingerprints'])),
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
    return dict(status=status, method=method, files=files, host_verify_rc=host_rc,
                review=os.path.relpath(os.path.join(out, 'REVIEW.md'), state.ROOT),
                proposed=state.now())


def host_verify(g, out, files, sig, data):
    """Re-run sqv on the host with the new keyrings (data only, no spec code).
    Returns (rc or None, review lines)."""
    if not [f for f in files if f.get('changed')]:
        return None, []
    sig_h, data_h = phase1.host_path(sig or '', g), phase1.host_path(data or '', g)
    for f in files:
        if f.get('kind') == 'signature' and f.get('changed'):
            sig_h = os.path.join(out, f['file'])
    rings = [os.path.join(out, f['file']) if f.get('changed') else os.path.join(g, f['file'])
             for f in files if 'fingerprints' in f]
    rings = ' '.join('--keyring=' + shlex.quote(r) for r in rings)
    # Data on stdin: the spec decompresses the source file next to the signature.
    if data == '-' and sig_h and os.path.isfile(sig_h):
        base = sig_h.rsplit('.', 1)[0]
        for ext, tool in (('.xz', 'xzcat'), ('.gz', 'zcat'), ('.bz2', 'bzcat'), ('.zst', 'zstdcat')):
            if os.path.isfile(base + ext):
                c = 'set -o pipefail; %s %s | sqv %s --signature-file %s -' % (
                    tool, shlex.quote(base + ext), rings, shlex.quote(sig_h))
                shown = '$ %s %s | sqv ... -' % (tool, os.path.basename(base + ext))
                break
        else:
            c = None
    elif sig_h and data_h and os.path.isfile(sig_h) and os.path.isfile(data_h):
        c = 'sqv %s --signature-file %s %s' % (rings, shlex.quote(sig_h), shlex.quote(data_h))
        shown = '$ sqv ... %s' % os.path.basename(data_h)
    else:
        c = None
    if not c:
        return None, ['Host verification skipped (data from stdin or a generated file); '
                      'run phase1.py after approval.', '']
    p = sh(['bash', '-c', c], timeout=900)
    return p.returncode, ['## Verification with the refreshed keyring', '', '```', shown,
                          (p.stdout + p.stderr).strip(), 'rc=%d' % p.returncode, '```', '']


def new_signature(sig, url, g, out):
    """The release signature upstream re-made (after refreshing its key), from URL,
    in place of SIG. Returns (file entry, review lines)."""
    src = phase1.host_path(sig or '', g)
    if not src:
        return dict(file=sig, kind='signature', error='signature not in dist-git'), []
    rel = os.path.relpath(src, g)
    dst = os.path.join(out, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    p = sh(['curl', '-fsSL', '-o', dst, url], timeout=300)
    info = dict(file=rel, kind='signature', method='signature-url', url=url,
                size_old=os.path.getsize(src) if os.path.exists(src) else None)
    if p.returncode or not os.path.exists(dst):
        info['error'] = 'download failed: %s' % (p.stderr.strip() or p.returncode)
        return info, []
    info['size_new'] = os.path.getsize(dst)
    info['sha256_new'] = hashlib.sha256(open(dst, 'rb').read()).hexdigest()
    info['changed'] = not os.path.exists(src) or open(src, 'rb').read() != open(dst, 'rb').read()
    dump = sh(['sq', '--home=none', 'packet', 'dump', dst]).stdout
    info['signatures'] = []
    for block in re.split(r'\n(?=\S)', dump):
        if not block.startswith('Signature Packet'):
            continue
        field = {k: re.search(r'(?m)^\s+%s: (.+)$' % k, block)
                 for k in ('Hash algo', 'Signature creation time', 'Issuer Fingerprint', 'Issuer')}
        if field['Hash algo'] and field['Signature creation time'] and \
                (field['Issuer Fingerprint'] or field['Issuer']):
            info['signatures'].append(dict(
                hash=field['Hash algo'].group(1).strip(),
                created=field['Signature creation time'].group(1).replace(' UTC', '').strip(),
                issuer=(field['Issuer Fingerprint'] or field['Issuer']).group(1).strip()))
    if not info['signatures']:
        info['error'] = 'no signature with hash, creation time and issuer in the file'
    lines = ['## %s (new release signature)' % rel, '', '- from: %s' % url,
             '- size: %s → %s bytes' % (info['size_old'], info['size_new'])] + \
        ['- %s, made %s, by `%s`' % (x['hash'], x['created'], x['issuer'])
         for x in info.get('signatures', [])] + \
        (['- **error: %s**' % info['error']] if info.get('error') else []) + ['']
    return info, lines


def propose(pkg, rec, sig_url=None):
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
            sh(['fedpkg', '--path', g, '--name', pkg, 'sources', '--force'], timeout=900)
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
    if sig_url:
        info, lines = new_signature(sig, sig_url, g, out)
        files.append(info)
        review += lines
    changed = [f for f in files if f.get('changed')]
    host_rc, verify = host_verify(g, out, files, sig, data)
    review += verify
    shutil.rmtree(tmp, ignore_errors=True)
    if any(f.get('kind') == 'signature' and f.get('error') for f in files):
        status = 'not-found'
    elif not changed:
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


GPG_TMP = 'GNUPGHOME="$(mktemp -d)" sh -c '


def gpg_export(src, dst, tmp):
    """Plain export of what GnuPG reads from keyring SRC (it skips PGP 2 / v3
    keys, which sq and sqv refuse to parse). Returns the number skipped."""
    h = tempfile.mkdtemp(dir=tmp)
    p = sh(['gpg', '--homedir', h, '--batch', '--import', src])
    sh(['gpg', '--homedir', h, '--batch', '--export', '--output', dst])
    m = re.search(r'skipped PGP-2 keys: (\d+)', p.stderr)
    return int(m.group(1)) if m else 0


def signers(sig, keyring):
    """Primary fingerprints of the certificates in KEYRING whose primary key
    or subkey made a signature in SIG."""
    issuers = set(re.findall(r'Issuer Fingerprint: ([0-9A-F]{40,64})',
                             sh(['sq', 'packet', 'dump', sig]).stdout))
    out = []
    for cert in re.split(r'(?m)^(?=\s*Fingerprint: )', sh(['sq', 'inspect', keyring]).stdout):
        keys = re.findall(r'(?:Fingerprint|Subkey): ([0-9A-F]{40,64})', cert)
        if keys and issuers & set(keys):
            out.append(keys[0])
    return out


def convert_recipe(mode, name, url, fprs):
    """Commands that make keyring NAME: the signing key(s) from keyservers, or
    upstream's KEYS file at URL converted by GnuPG (which drops the v3 keys
    sqv cannot read)."""
    if mode == 'signers':
        return recipe(name, fprs)
    dl = url.rsplit('/', 1)[-1]
    return ['curl -fsSL -O %s' % url,
            GPG_TMP + "'gpg --batch --import %s; gpg --batch --export --output %s'" % (dl, name),
            'rm %s' % dl]


def propose_convert(pkg, rec, mode, new_name=None, url=None):
    """A keyring sqv cannot read (v3 keys) or that holds stale keys, rebuilt
    with convert_recipe(). NEW_NAME renames the file (its Source line then
    names it instead of the upstream URL whose content it no longer is)."""
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
    for f in (sig, data):
        h = phase1.host_path(f or '', g)
        if h and not os.path.exists(h):
            sh(['fedpkg', '--path', g, '--name', pkg, 'sources', '--force'], timeout=900)
            break
    if len(keyrings) != 1:
        return dict(status='error', note='propose-convert handles one keyring per call')
    src = phase1.host_path(keyrings[0], g)
    rel = os.path.relpath(src, g)
    # The converted KEYS must not overwrite the download it is made from.
    name = new_name or os.path.basename(rel) + ('.pgp' if mode == 'gpg-export' else '')
    spec = open(os.path.join(g, pkg + '.spec')).read()
    if mode == 'gpg-export' and not url:
        urls = key_urls(spec, pkg, os.path.basename(rel))
        # The Source URL itself, not a page the comment above it links to.
        url = ([u for u in urls if u.rsplit('/', 1)[-1] == os.path.basename(rel)] or
               urls or [None])[0]
        if not url:
            return dict(status='error', note='no URL for %s in the spec; pass --url' % rel)
    base = os.path.join(tmp, 'old.pgp')
    skipped = gpg_export(src, base, tmp)
    old = fingerprints(base)
    sig_h = phase1.host_path(sig, g)
    fprs = signers(sig_h, base) if mode == 'signers' else None
    if mode == 'signers' and not fprs:
        return dict(status='error', note='the signing key is not in %s' % rel)
    cmds = convert_recipe(mode, name, url, fprs)
    run = os.path.join(tmp, 'run')
    os.makedirs(run)
    info = dict(file=rel, method='keyserver-signers' if mode == 'signers' else 'gpg-export',
                size_old=os.path.getsize(src), skipped_v3=skipped, commands=cmds,
                spec_commands=cmds, found_via=[], url=url,
                spec_header='# The key(s) that sign releases, from keyservers:'
                if mode == 'signers' else
                '# Upstream\'s KEYS file, converted by GnuPG (sqv cannot read the v3 keys in it):')
    if name != os.path.basename(rel):
        info['new_file'] = os.path.join(os.path.dirname(rel), name)
        urls = key_urls(spec, pkg, os.path.basename(rel))
        info['old_source'] = ([u for u in urls if u.rsplit('/', 1)[-1] ==
                               os.path.basename(rel)] or [None])[0]
    for c in cmds:
        p = sh(['bash', '-o', 'pipefail', '-c', c], cwd=run, timeout=600)
        info['found_via'] += sorted(set(re.findall(r'found via: (.*)', p.stdout + p.stderr)))
        if p.returncode:
            info['error'] = 'command failed: %s: %s' % (c, (p.stderr or '').strip()[-300:])
            break
    result = os.path.join(run, name)
    new = fingerprints(result) if os.path.exists(result) else []
    if not info.get('error') and mode == 'signers' and sorted(new) != sorted(fprs):
        info['error'] = 'keyservers returned a different set of certificates'
    if not info.get('error') and not new:
        info['error'] = 'no certificates in the result'
    files = [info]
    if not info.get('error'):
        dst = os.path.join(out, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(result, dst)
        info.update(changed=True, fingerprints=new, size_new=os.path.getsize(dst),
                    sha256_new=hashlib.sha256(open(dst, 'rb').read()).hexdigest(),
                    signers=signers(sig_h, dst),
                    dropped=[f for f in old if f not in new],
                    added=[f for f in new if f not in old])
    review = ['# Keyring %s for %s' % ('signing key(s) from keyservers' if mode == 'signers'
                                       else 'conversion of upstream KEYS', pkg), '',
              'Failing call: `%s`' % bad[0]['args'], '',
              'Phase 1 reason: `%s`' % res.get('failure_reason'), '',
              '## %s%s' % (rel, ' → %s' % info['new_file'] if info.get('new_file') else ''), '',
              '- v3 (PGP 2) keys in the old keyring, unreadable for sqv: %d' % skipped,
              '- certificates GnuPG reads in the old keyring: %d' % len(old),
              '- certificates in the new keyring: %s' % ', '.join(new),
              '- dropped: %s' % (', '.join(info.get('dropped') or []) or '-'),
              '- added: %s' % (', '.join(info.get('added') or []) or '-'),
              '- found via: %s' % ('; '.join(info['found_via']) or '-'),
              '- size: %s → %s bytes' % (info['size_old'], info.get('size_new', '-')),
              '', 'Commands (run in a copy of dist-git):', '', '```', *cmds, '```']
    if info.get('error'):
        review.append('- **error: %s**' % info['error'])
    else:
        old_s, new_s = os.path.join(tmp, 'old.summary'), os.path.join(tmp, 'new.summary')
        keep = set(new)
        open(old_s, 'w').write('\n'.join(summary(base)) + '\n')
        open(new_s, 'w').write('\n'.join(summary(os.path.join(out, rel))) + '\n')
        p = sh(['diff', '-u', '--label', 'dist-git/' + rel + ' (as GnuPG reads it)',
                '--label', 'new/' + name, old_s, new_s], timeout=60)
        # Only the kept certificates matter for review; a KEYS diff is long.
        review += ['', '```diff', p.stdout.rstrip()[:20000] or '(no change)', '```'] \
            if mode == 'signers' or len(keep) <= 5 else []
        if info['size_new'] > FLOOD_LIMIT:
            info['warning'] = 'keyring is %d bytes' % info['size_new']
            review.append('- **warning: %s**' % info['warning'])
    review.append('')
    host_rc, verify = host_verify(g, out, files, sig, data)
    review += verify
    shutil.rmtree(tmp, ignore_errors=True)
    status = 'not-found' if info.get('error') else \
        'still-fails' if host_rc not in (None, 0) else 'proposed'
    review.insert(2, '**Status: %s**' % status)
    review.insert(3, '')
    text = '\n'.join(review) + '\n'
    open(os.path.join(out, 'REVIEW.md'), 'w').write(text)
    shared = os.path.join(state.ROOT, 'reports', 'keyring-refresh')
    os.makedirs(shared, exist_ok=True)
    open(os.path.join(shared, pkg + '.md'), 'w').write(text)
    return dict(status=status, method=info['method'], files=files, host_verify_rc=host_rc,
                review=os.path.relpath(os.path.join(out, 'REVIEW.md'), state.ROOT),
                proposed=state.now())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('action', choices=['propose', 'propose-upstream', 'propose-key',
                                       'propose-convert', 'show', 'approve', 'reject'])
    ap.add_argument('packages', nargs='*')
    ap.add_argument('--note', default=None)
    ap.add_argument('--url', default=None,
                    help='propose-upstream/propose-key: take the key from this URL')
    ap.add_argument('--source-url', action='store_true',
                    help='propose-upstream: make the Source line the URL and name the file '
                         'like it, instead of a comment with the commands')
    ap.add_argument('--replace', action='store_true',
                    help='propose-upstream: the URL file may hold fewer keys; the others go')
    ap.add_argument('--superset', action='store_true',
                    help='propose-upstream: the URL file may hold more keys; they are added')
    ap.add_argument('--keyserver', action='store_true',
                    help='propose-key: complete the key from keyservers/WKD')
    ap.add_argument('--signers', action='store_true',
                    help='propose-convert: only the key(s) that signed the release, '
                         'from keyservers')
    ap.add_argument('--gpg-export', action='store_true',
                    help='propose-convert: upstream\'s KEYS file (--url or the spec\'s '
                         'Source URL) converted by GnuPG')
    ap.add_argument('--new-name', default=None,
                    help='propose-convert: the file name of the new keyring')
    ap.add_argument('--signature-url', default=None,
                    help='propose: also replace the release signature with the one upstream '
                         're-made at this URL (after refreshing its key)')
    ap.add_argument('--pr-note', default=None,
                    help='propose, propose-convert: a paragraph for the PR description')
    a = ap.parse_args()
    st = state.load()
    if a.action == 'propose-convert':
        if a.signers == a.gpg_export or not a.packages:
            ap.error('propose-convert needs packages and one of --signers, --gpg-export')
        for pkg in a.packages:
            try:
                kr = propose_convert(pkg, st[pkg], 'signers' if a.signers else 'gpg-export',
                                     a.new_name, a.url)
            except Exception as e:  # one broken package must not stop the run
                kr = dict(status='error', note='refresh_keys: %r' % e, proposed=state.now())
            if a.pr_note:
                kr['pr_note'] = a.pr_note
            with phase1.LOCK:
                cur = state.load()
                cur[pkg]['keyring_refresh'] = kr
                cur[pkg]['updated'] = state.now()
                state.save(cur)
            print('%-28s %s %s' % (pkg, kr['status'], kr.get('note') or ''), flush=True)
        return 0
    if a.signature_url and (a.action != 'propose' or len(a.packages) != 1):
        ap.error('--signature-url needs propose and exactly one package')
    if a.action == 'propose':
        pkgs = a.packages or sorted(
            p for p, r in st.items() if r.get('status') == 'regression' and
            (r.get('results') or [{}])[0].get('failure_reason') in REFRESHABLE)
        for pkg in pkgs:
            try:
                kr = propose(pkg, st[pkg], a.signature_url)
                if a.pr_note:
                    kr['pr_note'] = a.pr_note
            except Exception as e:  # one broken package must not stop the run
                kr = dict(status='error', note='refresh_keys: %r' % e, proposed=state.now())
            with phase1.LOCK:
                cur = state.load()
                cur[pkg]['keyring_refresh'] = kr
                cur[pkg]['updated'] = state.now()
                state.save(cur)
            print('%-28s %s' % (pkg, kr['status']), flush=True)
        return 0
    if a.action == 'propose-key' and not (a.url and a.packages):
        ap.error('propose-key needs --url and packages')
    if a.action in ('propose-upstream', 'propose-key'):
        pkgs = a.packages or sorted(p for p, r in st.items() if r.get('status') == 'regression')
        for pkg in pkgs:
            try:
                up = propose_upstream(pkg, st[pkg], a.url,
                                      a.keyserver if a.action == 'propose-key' else None,
                                      a.replace, a.source_url, a.superset)
            except Exception as e:  # one broken package must not stop the run
                up = dict(status='error', method=a.action, note='%r' % e)
            d = os.path.join(phase1.WORK, pkg)
            with phase1.LOCK:
                cur = state.load()
                r = cur[pkg]
                r['upstream_key'] = {k: v for k, v in up.items() if k != 'files'}
                if up['status'] == 'proposed':
                    # Preferred over a keyserver refresh: it is what the spec names.
                    if r.get('keyring_refresh', {}).get('method') not in UPSTREAM_METHODS:
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
