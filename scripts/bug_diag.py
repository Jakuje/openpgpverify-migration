"""Full diagnosis of a failing release signature: every problem, not just sqv's first.

Usage: bug_diag.py check OUTDIR PKG... > diag.jsonl   one JSON line per package
       bug_diag.py apply diag.jsonl                   bug_reason + bug_findings into the state

check reads the signature and keyring of the tested dist-git commit (work/PKG/dist-git,
or its lookaside) and the signing key as `sq network search` finds it (keyservers,
WKD). apply picks the bug text from all problems found and lists the packages
whose network copy of the key has none (candidates for refresh_keys.py propose).
"""
import datetime, json, os, re, subprocess, sys, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import state  # noqa: E402

ROOT = os.path.expanduser('~/devel/openpgpverify-migration')
WEAK_HASH = ('SHA1', 'MD5', 'RipeMD')


def run(cmd, timeout=300):
    return subprocess.run(cmd, capture_output=True, timeout=timeout)


def ts(s):
    s = s.replace(' (critical)', '').replace(' UTC', '').strip()
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S').replace(tzinfo=datetime.timezone.utc)


def fetch(pkg, g, name, out):
    """A file of the tested commit: from git, or from the lookaside by its sources hash."""
    dst = os.path.join(out, name)
    r = run(['git', '-C', g, 'show', 'HEAD:' + name])
    if r.returncode == 0:
        open(dst, 'wb').write(r.stdout)
        return dst
    src = run(['git', '-C', g, 'show', 'HEAD:sources']).stdout.decode()
    m = re.search(r'^SHA512 \(%s\) = (\w+)$' % re.escape(name), src, re.M)
    algo = 'sha512'
    if not m:
        m, algo = re.search(r'^(\w{32})  %s$' % re.escape(name), src, re.M), 'md5'
    if not m:
        return None
    url = 'https://src.fedoraproject.org/repo/pkgs/rpms/%s/%s/%s/%s/%s' % (
        pkg, name, algo, m.group(1), name)
    with urllib.request.urlopen(url, timeout=120) as u:
        open(dst, 'wb').write(u.read())
    return dst


def packets(path):
    """sq packet dump, split into (header, {field: [values]}) per packet."""
    r = run(['sq', '--home=none', 'packet', 'dump', path])
    out = []
    for block in re.split(r'\n(?=\S)', r.stdout.decode(errors='replace')):
        lines = block.split('\n')
        f = {}
        for l in lines[1:]:
            m = re.match(r'\s+([A-Za-z][\w -]*?): (.*)$', l)
            if m:
                f.setdefault(m.group(1), []).append(m.group(2).strip())
        out.append((lines[0], f))
    return out, r.stderr.decode(errors='replace')


def first(f, k):
    return (f.get(k) or [None])[0]


def certs(path):
    """Certificates with their keys and self-signatures."""
    pk, err = packets(path)
    res, cur, key = [], None, None
    for h, f in pk:
        if h.startswith('Public-Key Packet') or h.startswith('Secret-Key Packet'):
            cur = dict(fpr=first(f, 'Fingerprint'), keyid=first(f, 'KeyID'), keys=[], sigs=[],
                       version=first(f, 'Version'))
            key = dict(fpr=cur['fpr'], keyid=cur['keyid'], algo=first(f, 'Pk algo'),
                       size=first(f, 'Pk size'), created=first(f, 'Creation time'),
                       primary=True, bindings=[])
            cur['keys'].append(key)
            res.append(cur)
        elif h.startswith('Public-Subkey') and cur:
            key = dict(fpr=first(f, 'Fingerprint'), keyid=first(f, 'KeyID'),
                       algo=first(f, 'Pk algo'), size=first(f, 'Pk size'),
                       created=first(f, 'Creation time'), primary=False, bindings=[])
            cur['keys'].append(key)
        elif h.startswith('Signature Packet') and cur:
            issuer = (f.get('Issuer') or [''])[0]
            ifpr = (f.get('Issuer Fingerprint') or [''])[0]
            if issuer != cur['keyid'] and ifpr != cur['fpr']:
                continue        # third-party certification
            # A signing subkey's binding embeds a back-signature (PrimaryKeyBinding),
            # whose hash counts as well: sq lists its fields after the outer ones.
            s = dict(type=first(f, 'Type'), hash=first(f, 'Hash algo'),
                     back_hash=(f.get('Hash algo') or [None, None])[1:2] and
                     f['Hash algo'][1],
                     created=(first(f, 'Signature creation time') or '').replace(' UTC', ''),
                     key_expiry=first(f, 'Key expiration time'))
            if s['type'] in ('SubkeyBinding', 'SubkeyRevocation'):
                key['bindings'].append(s)
            else:
                cur['keys'][0]['bindings'].append(s)
    return res, err


def parse_dur(s, created):
    """'Key expiration time' as an absolute time: sq prints a duration plus the date."""
    if not s:
        return None
    m = re.search(r'(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)', s)
    if m:
        return ts(m.group(1))
    secs = 0
    for n, u in re.findall(r'(\d+)([ywdhms])', s):
        secs += int(n) * dict(y=31557600, w=604800, d=86400, h=3600, m=60, s=1)[u]
    return ts(created.replace(' UTC', '')) + datetime.timedelta(seconds=secs) if secs else None


def weak_key(k):
    a, size = (k['algo'] or ''), int(re.sub(r'\D', '', k['size'] or '0') or 0)
    if a.startswith('DSA') or a.startswith('ElGamal'):
        return '%s-%d' % (a.split()[0], size)
    if a.startswith('RSA') and size < 2048:
        return 'RSA-%d' % size
    return None


def key_problems(c, k, t):
    """What is wrong with key k of cert c at signature time t."""
    p = []
    prim = c['keys'][0]
    for kk in ([prim] if k is prim else [prim, k]):
        w = weak_key(kk)
        if w:
            p.append('weak-key:%s%s' % ('subkey ' if not kk['primary'] else
                                        '' if k is prim else 'primary key ', w))
        sigs = [s for s in kk['bindings'] if s['type'] and 'Revocation' not in s['type']]
        before = [s for s in sigs if s['created'] and ts(s['created']) <= t]
        if not before:
            p.append('binding-after-signature:%s' % ('primary' if kk['primary'] else 'subkey'))
            continue
        good = [s for s in before if s['hash'] not in WEAK_HASH and
                s.get('back_hash') not in WEAK_HASH]
        if not good:
            p.append('sha1-binding:%s' % ('primary' if kk['primary'] else 'subkey'))
        latest = max(good or before, key=lambda s: s['created'])
        exp = parse_dur(latest['key_expiry'], kk['created'])
        if exp and exp < t:
            p.append('expired:%s %s' % ('primary' if kk['primary'] else 'subkey',
                                        exp.strftime('%Y-%m-%d')))
    return p


def analyse(keyring, sigs):
    cs, err = certs(keyring)
    res = dict(certs=len(cs), parse_errors='unknown version' in err or 'Malformed' in err,
               v3_keys=sum(1 for c in cs if c['version'] == '3'))
    per = []
    for s in sigs:
        t = ts(s['created'])
        match = [(c, k) for c in cs for k in c['keys']
                 if s['issuer'] and (k['fpr'] == s['issuer'] or k['keyid'] == s['issuer'][-16:])]
        if not match:
            per.append(dict(issuer=s['issuer'], problems=['not-in-keyring']))
            continue
        c, k = match[0]
        prim = c['keys'][0]
        per.append(dict(issuer=s['issuer'], primary=c['fpr'], key=k['fpr'],
                        algo='%s %s' % (k['algo'], k['size']),
                        primary_algo='%s %s' % (prim['algo'], prim['size']),
                        problems=key_problems(c, k, t)))
    res['per_sig'] = per
    return res


def check(out, pkg):
    g = os.path.join(ROOT, 'work', pkg, 'dist-git')
    bug = open(os.path.join(ROOT, 'proposals', pkg, 'BUG.md')).read()
    call = re.search(r'%openpgpverify ([^\n]*)', bug).group(1)
    kname = re.search(r'--keyring=(\S+)', call).group(1)
    sname = re.search(r'--signature=(\S+)', call).group(1)
    d = os.path.join(out, pkg)
    os.makedirs(d, exist_ok=True)
    res = dict(package=pkg, commit=run(['git', '-C', g, 'rev-parse', '--short=12', 'HEAD']
                                       ).stdout.decode().strip())
    kf, sf = fetch(pkg, g, kname, d), fetch(pkg, g, sname, d)
    if not kf or not sf:
        return dict(res, error='missing %s' % ('keyring' if not kf else 'signature'))
    sigs = []
    for h, f in packets(sf)[0]:
        if h.startswith('Signature Packet'):
            sigs.append(dict(version=first(f, 'Version'), hash=first(f, 'Hash algo'),
                             algo=first(f, 'Pk algo'),
                             created=(first(f, 'Signature creation time') or
                                      first(f, 'Creation time') or '').replace(' UTC', ''),
                             issuer=first(f, 'Issuer Fingerprint') or first(f, 'Issuer')))
    res['sigs'] = sigs
    res['sig_problems'] = sorted({p for s in sigs for p in
                                  (['v3-sig'] if s['version'] == '3' else []) +
                                  (['sha1-data:%s' % s['hash']] if s['hash'] in WEAK_HASH else [])})
    if not sigs or not sigs[0]['created']:
        return dict(res, error='cannot read signature')
    res['distgit'] = analyse(kf, sigs)
    ks = {}
    for s in sigs:
        fpr = s['issuer']
        o = os.path.join(d, 'ks-%s.pgp' % fpr[-16:])
        r = run(['sq', '--home=none', 'network', 'search', fpr, '--output', o, '--overwrite'],
                timeout=180)
        if r.returncode or not os.path.exists(o):
            r = run(['sq', '--home=none', 'network', 'keyserver', 'search', fpr, '--output', o,
                     '--overwrite'], timeout=180)
        if not r.returncode and os.path.exists(o):
            ks[fpr] = analyse(o, [s])['per_sig'][0]
        else:
            ks[fpr] = dict(problems=['not-found'])
    res['network'] = ks
    return res


LABEL = {'weak-key': 'key algorithm rejected by the crypto policy (%s)',
         'sha1-data': 'the release signature uses SHA-1',
         'v3-sig': 'the release signature is in the version 3 format',
         'sha1-binding': 'the key\'s self-signatures use only SHA-1',
         'expired': 'the key had expired when the release was signed (%s)',
         'binding-after-signature': 'the key has no self-signature from before the release '
                                    'signature',
         'not-in-keyring': 'the signing key is not in the keyring'}


def problems(per):
    """{kind: [details]} for the problems of one key."""
    out = {}
    for p in per['problems']:
        k, _, d = p.partition(':')
        out.setdefault(k, []).append(d)
    return out


def describe(p):
    out = []
    for k, ds in p.items():
        if k == 'weak-key':
            out.append(LABEL[k] % ', '.join(d.replace('subkey ', 'signing subkey ') if
                                            d.startswith('subkey ') else d for d in ds))
        elif k == 'expired':
            out.append(LABEL[k] % ', '.join(sorted({'on ' + d.split()[-1] for d in ds})))
        elif k in LABEL:
            out.append(LABEL[k])
    return out


def choose(d, prev):
    """Bug reason from all problems; None when the network key would fix it."""
    sig = {p.split(':')[0] for p in d['sig_problems']}
    dg, nw = {}, {}
    for s in d['distgit']['per_sig']:
        dg.update(problems(s))
    for v in d['network'].values():
        nw.update(problems(v))
    found = 'not-found' not in nw
    if 'weak-key' in dg:
        return 'weak-key', sig, dg, nw
    if prev == 'v3-key-sha1-cert':
        return prev, sig, dg, nw
    if 'sha1-data' in sig or 'v3-sig' in sig:
        return ('sha1-sig-and-cert' if 'sha1-binding' in (nw if found else dg) else 'sha1-sig',
                sig, dg, nw)
    if found and not nw:
        return None, sig, dg, nw
    if 'sha1-binding' in dg or 'sha1-binding' in nw:
        return 'sha1-cert', sig, dg, nw
    if 'expired' in dg:
        return 'expired', sig, dg, nw
    if 'binding-after-signature' in dg:
        return 'binding-after-signature', sig, dg, nw
    return prev, sig, dg, nw


def hash_name(h):
    return re.sub(r'^SHA(\d)', r'SHA-\1', h or '?')


SHA1_WHY = ('SHA-1 is no longer considered secure: collisions have been practical since '
            '2017 (SHAttered) and chosen-prefix collisions since 2020 (SHA-1 is a Shambles), '
            'and the crypto policy rejects it')
NETWORK = 'keys.openpgp.org, keyserver.ubuntu.com and WKD'


def findings(d, sig, dg, nw, v3_keyring=False):
    """Markdown: what the signature is, then one item per problem with the reason."""
    s0 = d['sigs'][0]
    k0 = d['distgit']['per_sig'][0]
    made = s0['created'].split()[0]
    sub = k0.get('key') and k0['key'] != k0.get('primary')
    if sub:
        by = 'the subkey `%s` (%s) of the key `%s` (%s)' % (
            k0['key'], k0['algo'], k0['primary'], k0['primary_algo'])
    else:
        by = 'the key `%s` (%s)' % (k0.get('primary') or s0['issuer'], k0.get('algo') or '?')
    head = ('The release signature (%s, made %s) is by %s. sqv reports only the first '
            'problem it hits (above). All the problems found:' % (hash_name(s0['hash']), made,
                                                                 by))
    items = []
    for kind, ds in sorted(dg.items(), key=lambda x: x[0] != 'weak-key'):
        if kind == 'weak-key':
            for x in ds:
                what = ('The signing subkey' if x.startswith('subkey ') else
                        'The primary key' if x.startswith('primary key ') or sub else
                        'The key')
                alg = x.split()[-1]
                items.append(
                    '%s is %s. DSA keys and RSA keys shorter than 2048 bits are no longer '
                    'considered secure, and the crypto policy rejects them.%s' % (
                        what, alg,
                        ' The release is signed by the subkey, but the primary key that '
                        'binds the subkey counts too.'
                        if x.startswith('primary key ') or (sub and what == 'The primary key')
                        else ''))
                if alg == 'DSA-1024' and 'sha1-data' in sig and not sub:
                    items[-1] += (' DSA-1024 can only use 160-bit hashes, which is also why '
                                  'its signatures are SHA-1.')
        elif kind == 'sha1-binding':
            items.append(
                'The self-signatures that bind the key\'s user IDs%s to it use only SHA-1. '
                '%s. GnuPG doesn\'t check self-signatures; Sequoia does, and without a valid '
                'one it doesn\'t use the key at all.' % (
                    ' and subkeys' if any(x == 'subkey' for x in ds) or sub else '',
                    SHA1_WHY))
        elif kind == 'expired':
            dates = sorted({x.split()[-1] for x in ds})
            items.append(
                'The key expired on %s, before the release was signed on %s, according to '
                'the keyring in dist-git. GnuPG ignores expiry; Sequoia checks that the key '
                'was valid when the signature was made.' % (', '.join(dates), made))
        elif kind == 'binding-after-signature':
            items.append(
                'The keyring in dist-git has no self-signature%s from before %s, when the '
                'release was signed, so for Sequoia the key wasn\'t valid yet at that '
                'time.' % (' for the signing subkey' if ds == ['subkey'] else '', made))
    if 'v3-sig' in sig:
        items.append('The release signature is in the version 3 (PGP 2) format, which '
                     'current OpenPGP implementations no longer accept.')
    if 'sha1-data' in sig:
        items.append('The release signature itself uses SHA-1 too; for signatures over '
                     'data, this won\'t be relaxed.' if 'sha1-binding' in dg else
                     'The release signature itself uses SHA-1. %s; for signatures over '
                     'data, this won\'t be relaxed.' % SHA1_WHY)
    if v3_keyring:
        items.append('The keyring also contains a version 3 key, which Sequoia can\'t '
                     'parse. GnuPG skips it silently; sqv rejects the whole keyring.')
    if dg:
        if 'not-found' in nw:
            net = 'The key is not published on %s.' % NETWORK
        elif set(nw) == set(dg):
            net = 'The copy of the key on %s has the same problems.' % NETWORK
        elif nw:
            net = ('The copy of the key on %s is newer, but its problems remain: %s.'
                   % (NETWORK, ', '.join(sorted(LABEL[k].split(' (')[0] for k in nw))))
        else:
            net = 'The copy of the key on %s has none of these problems.' % NETWORK
    else:
        net = 'The key itself is fine.'
    return head + '\n\n' + '\n'.join('- ' + i for i in items) + '\n\n' + net


def apply(path):
    st = state.load()
    refresh = []
    for l in open(path):
        d = json.loads(l)
        if 'error' in d:
            print('%-24s skipped: %s' % (d['package'], d['error']))
            continue
        s = st[d['package']]
        reason, sig, dg, nw = choose(d, s.get('bug_reason'))
        if reason is None:
            refresh.append(d['package'])
            s.pop('bug_reason', None)
            s.pop('bug_findings', None)
            print('%-24s network key is clean: try refresh_keys.py propose' % d['package'])
            continue
        s['bug_reason'] = reason
        s['bug_findings'] = findings(d, sig, dg, nw, reason == 'v3-key-sha1-cert')
        s['bug_diag_commit'] = d['commit']
        print('%-24s %s' % (d['package'], reason))
    state.save(st)
    return refresh


if __name__ == '__main__':
    if sys.argv[1] == 'apply':
        apply(sys.argv[2])
        sys.exit(0)
    out = sys.argv[2]
    for pkg in sys.argv[3:]:
        try:
            r = check(out, pkg)
        except Exception as e:
            r = dict(package=pkg, error='checker: %r' % e)
        print(json.dumps(r), flush=True)
