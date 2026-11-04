"""Sort proposed keyring refreshes by where a current upstream copy of the key
can be fetched: python3 -I upsort.py OUT.jsonl PKG...  (read-only on the repo)"""
import concurrent.futures, hashlib, json, os, re, subprocess, sys, tempfile

ROOT = os.path.expanduser('~/devel/openpgpverify-migration')
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import refresh_keys  # noqa: E402

ZB32 = 'ybndrfg8ejkmcpqxot1uwisza345h769'
KERNEL = 'https://git.kernel.org/pub/scm/docs/kernel/pgpkeys.git/plain/keys/%s.asc'
VKS = 'https://keys.openpgp.org/vks/v1/by-fingerprint/%s'
st = {json.loads(l)['package']: json.loads(l) for l in open(os.path.join(ROOT, 'data/state/packages.jsonl'))}


def zbase32(b):
    bits = ''.join('%08d' % int(bin(x)[2:]) for x in b)
    return ''.join(ZB32[int(bits[i:i + 5].ljust(5, '0'), 2)] for i in range(0, len(bits), 5))


def wkd(email):
    local, dom = email.rsplit('@', 1)
    h = zbase32(hashlib.sha1(local.lower().encode()).digest())
    dom = dom.lower()
    return ['https://openpgpkey.%s/.well-known/openpgpkey/%s/hu/%s?l=%s' % (dom, dom, h, local),
            'https://%s/.well-known/openpgpkey/hu/%s?l=%s' % (dom, h, local)]


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, timeout=300, **kw)


def certs(path):
    out = run(['sq', '--home=none', 'inspect', path]).stdout.decode(errors='replace')
    fprs = re.findall(r'(?m)^\s+Fingerprint: ([0-9A-F]{40})', out)
    emails = re.findall(r'(?m)^\s+UserID: .*<([^>\s]+@[^>\s]+)>', out)
    return fprs, emails


def check(pkg):
    r = st[pkg]
    kr = r['keyring_refresh']
    g = os.path.join(ROOT, 'work', pkg, 'dist-git')
    rep = open(os.path.join(ROOT, 'reports/keyring-refresh/%s.md' % pkg)).read()
    call = re.search(r'Failing call: `([^`]*)`', rep).group(1)
    sig = re.search(r'--signature=/builddir/new/(\S+)', call).group(1)
    data = re.search(r'--data=(\S+)', call).group(1)
    res = dict(package=pkg, sig=sig)
    if data == '-':
        base = sig.rsplit('.', 1)[0]
        cands = [f for f in os.listdir(g) if f.startswith(base + '.') and
                 not re.search(r'\.(sign|asc|sig)$', f)]
        if not cands:
            return dict(res, error='no local data for stdin')
        f = os.path.join(g, cands[0])
        dec = ['xzcat', f] if f.endswith('.xz') else ['zcat', f] if f.endswith('.gz') else \
            ['zstdcat', f] if f.endswith('.zst') else ['bzcat', f] if f.endswith('.bz2') else ['cat', f]
    else:
        f = os.path.join(g, data.replace('/builddir/new/', ''))
        dec = ['cat', f]
    if not os.path.exists(f) or not os.path.exists(os.path.join(g, sig)):
        return dict(res, error='sources not in work/ (pruned)')
    spec = open(os.path.join(g, pkg + '.spec')).read()
    want, emails, urls = [], [], []
    for fi in kr['files']:
        want += fi['fingerprints']
        e = certs(os.path.join(ROOT, 'work', pkg, 'refresh', fi['file']))[1]
        emails += e
        for u in refresh_keys.key_urls(spec, pkg, os.path.basename(fi['file'])):
            urls.append(('spec', u))
    for fp in want:
        urls.append(('kernel.org', KERNEL % fp[-16:]))
    for e in dict.fromkeys(emails):
        for u in wkd(e):
            urls.append(('wkd', u))
    for fp in want:
        urls.append(('keys.openpgp.org', VKS % fp))
    res.update(want=want, emails=list(dict.fromkeys(emails)), tried=[])
    with tempfile.TemporaryDirectory() as tmp:
        for i, (kind, u) in enumerate(dict.fromkeys(urls)):
            dl = os.path.join(tmp, 'k%d' % i)
            p = run(['curl', '-A', 'Mozilla/5.0', '-fsSL', '--max-time', '30', '-o', dl, u])
            if p.returncode or not os.path.exists(dl):
                res['tried'].append(dict(kind=kind, url=u, result='fetch failed'))
                continue
            fprs = certs(dl)[0]
            if not fprs:
                res['tried'].append(dict(kind=kind, url=u, result='no certificate'))
                continue
            d = subprocess.Popen(dec, stdout=subprocess.PIPE)
            v = subprocess.run(['sqv', '--keyring=' + dl, os.path.join(g, sig), '-'],
                               stdin=d.stdout, capture_output=True, timeout=600)
            d.wait()
            err = v.stderr.decode(errors='replace').strip().split('\n')[-1][:120]
            res['tried'].append(dict(kind=kind, url=u, fprs=fprs, size=os.path.getsize(dl),
                                     result='verifies' if v.returncode == 0 else err))
    return res


def safe(pkg):
    try:
        return check(pkg)
    except Exception as e:
        return dict(package=pkg, error='checker: %r' % e)


if __name__ == '__main__':
    out = open(sys.argv[1], 'w')
    with concurrent.futures.ThreadPoolExecutor(6) as ex:
        for res in ex.map(safe, sys.argv[2:]):
            out.write(json.dumps(res) + '\n')
            out.flush()
            ok = [t['kind'] for t in res.get('tried', []) if t.get('result') == 'verifies']
            print('%-26s %s' % (res['package'], res.get('error') or ', '.join(dict.fromkeys(ok)) or '-'),
                  flush=True)
