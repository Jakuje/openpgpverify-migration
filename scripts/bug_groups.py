"""Group the bug drafts by upstream signing key and by Fedora owner, for manual batches.

Usage: bug_groups.py DIAG.jsonl > reports/bug-groups-DATE.md

DIAG.jsonl is the output of `bug_diag.py check`; the signing key of each package is
the primary key that signed the release in the dist-git keyring. Owners come from
data/snapshots/latest/pagure_owner_alias.json. Key owner names come from the user
IDs of the keyring in the tested dist-git commit (fetched like bug_diag.py does).
"""
import collections, datetime, json, os, re, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import state  # noqa: E402
from bug_diag import fetch, packets  # noqa: E402
from render_proposals import REASONS  # noqa: E402
from bug_response import KINDS  # noqa: E402

BZ = 'https://bugzilla.redhat.com/show_bug.cgi?id=%s'


def uid_name(pkg, fpr, tmp):
    """Name in the first user ID of key fpr in the package's dist-git keyring."""
    path = os.path.join(state.ROOT, 'proposals', pkg, 'BUG.md')
    if not os.path.exists(path):    # the package became a PR (keyring refresh)
        return None
    bug = open(path).read()
    kname = re.search(r'--keyring=(\S+)', bug).group(1)
    d = os.path.join(tmp, pkg)
    os.makedirs(d, exist_ok=True)
    kf = fetch(pkg, os.path.join(state.ROOT, 'work', pkg, 'dist-git'), kname, d)
    if not kf:
        return None
    cur = None
    for h, f in packets(kf)[0]:
        if h.startswith('Public-Key Packet'):
            cur = (f.get('Fingerprint') or [''])[0]
        elif h.startswith('User ID Packet') and cur == fpr and f.get('Value'):
            return re.sub(r'\s*<[^>]*>', '', f['Value'][0]).strip() or None
    return None


def main():
    st = state.load()
    owners = json.load(open(os.path.join(state.ROOT, 'data/snapshots/latest/pagure_owner_alias.json')))['rpms']
    eln = set(open(os.path.join(state.ROOT, 'data/eln-in-scope.txt')).read().split())
    pkgs = sorted(p for p, s in st.items() if s.get('bug_reason'))
    diag = {}
    for l in open(sys.argv[1]):
        d = json.loads(l)
        diag[d['package']] = d

    bykey, byowner, names = collections.defaultdict(set), collections.defaultdict(set), {}
    with tempfile.TemporaryDirectory() as tmp:
        for p in pkgs:
            per = diag.get(p, {}).get('distgit', {}).get('per_sig', [])
            for k in {x.get('primary') or x.get('issuer') or '?' for x in per} or {'?'}:
                bykey[k].add(p)
                if not names.get(k) and len(k) == 40:
                    names[k] = uid_name(p, k, tmp)
            for o in owners.get(p, ['?']):
                byowner[o].add(p)

    def cell(p):
        s = st[p]
        draft = 'BUG.md' if os.path.exists(os.path.join(
            state.ROOT, 'proposals', p, 'BUG.md')) else 'PR.md'
        out = '[%s](../proposals/%s/%s)' % (p, p, draft)
        if p in eln:
            out += ' **ELN**'
        if s.get('bug_id'):
            out += ' ([filed](%s))' % (BZ % s['bug_id'])
        return out

    def problem(p):
        return REASONS[st[p]['bug_reason']][0]

    filed = sum(1 for p in pkgs if st[p].get('bug_id'))
    shared = [(k, ps) for k, ps in bykey.items() if len(ps) > 1]
    shared.sort(key=lambda x: (-len(x[1]), min(x[1])))
    big = [(o, ps) for o, ps in byowner.items() if len(ps) >= 3]
    big.sort(key=lambda x: (-len(x[1]), x[0]))
    single = sum(1 for ps in byowner.values() if len(ps) == 1)

    w = sys.stdout.write
    w('# Bug drafts grouped by upstream key and by owner, %s\n\n' % datetime.date.today())
    w('The %d bug drafts of [bugs-2026-11-09.md](bugs-2026-11-09.md) (%d filed so far, '
      'blocking the tracker [rhbz#2569052](%s)), grouped so that they can be handled in '
      'batches: one upstream contact for all packages signed with the same key, and one '
      'batch per Fedora owner with many packages.\n\n' % (len(pkgs), filed, BZ % 2569052))
    w('If you want to take an upstream contact or a batch before the bugs are filed, '
      'say so in the tracker, so the bug for those packages can point to it. Each '
      'package\'s draft (linked) has the failing `sqv` call, every problem found and '
      'the suggested fixes. **ELN** marks packages in the ELN buildroot.\n\n')

    w('## Upstream keys shared by several packages\n\n')
    w('%d keys sign the releases of %d packages. The key is the primary key that '
      'signed the release; the name is from its user ID.\n\n'
      % (len(shared), sum(len(ps) for _, ps in shared)))
    w('| Key | Name | Problem | Packages |\n|---|---|---|---|\n')
    for k, ps in shared:
        probs = sorted({problem(p) for p in ps})
        w('| `%s` | %s | %s | %s |\n' % (k, names.get(k) or '', '; '.join(probs),
                                         ', '.join(cell(p) for p in sorted(ps))))

    w('\n## Owners with three or more packages\n\n')
    w('%d owners in total; %d of them have one package only. A package can have '
      'several owners (main admin and co-maintainers), so it can appear in more than '
      'one row.\n\n' % (len(byowner), single))
    w('| Owner | Count | Packages |\n|---|---|---|\n')
    for o, ps in big:
        w('| %s | %d | %s |\n' % (o, len(ps), ', '.join(cell(p) for p in sorted(ps))))

    resp = sorted((p for p in pkgs if st[p].get('bug_response')),
                  key=lambda p: (st[p]['bug_response']['kind'], p))
    w('\n## Responses on the bugs\n\n')
    if resp:
        w('Recorded with `scripts/bug_response.py`. %d so far.\n\n' % len(resp))
        w('| Package | Response | Note | Date |\n|---|---|---|---|\n')
        for p in resp:
            r = st[p]['bug_response']
            link = (BZ % st[p]['bug_id']) + ('#c%d' % r['comment'] if r.get('comment') else '')
            w('| %s | %s | [%s](%s) | %s |\n' % (cell(p), KINDS[r['kind']], r['note'], link,
                                               r['date']))
    else:
        w('None recorded yet.\n')

    w('\n## All packages\n\n| Package | Problem | Key | Owners |\n|---|---|---|---|\n')
    for p in pkgs:
        ks = sorted(k for k, ps in bykey.items() if p in ps)
        w('| %s | %s | %s | %s |\n' % (cell(p), problem(p), ', '.join('`%s`' % k for k in ks),
                                       ', '.join(owners.get(p, []))))


if __name__ == '__main__':
    main()
