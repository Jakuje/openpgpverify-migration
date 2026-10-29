#!/usr/bin/python3 -I
"""Progress of the migration: where each package that verified sources with
GnuPG at the start stands today.

Usage: progress.py BASELINE.jsonl TODAY.jsonl OUT.md [--prs PRS.tsv] [--fetch]

BASELINE.jsonl  inventory of the snapshot when the work started (2026-10-06)
TODAY.jsonl     inventory of today's snapshot (classify.py)
--fetch         query Pagure for PRs of every relevant package and write PRS.tsv
--prs PRS.tsv   PR list (package, id, status, author, url, title, updated)

A package counts as converted when today's spec calls %openpgpverify and no
GnuPG verification is left (classify.py category "converted"). PRs are the
dist-git PRs whose title mentions openpgpverify or Sequoia, by anyone.
"""
import argparse
import collections
import concurrent.futures
import json
import os
import re
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import state  # noqa: E402

PAGURE = 'https://src.fedoraproject.org/api/0/rpms/%s/pull-requests?status=all&per_page=100'
BUGZILLA = ('https://bugzilla.redhat.com/rest/bug?blocks=2523619'
            '&include_fields=id,component,status,resolution,summary')
TRACKER = 'https://bugzilla.redhat.com/show_bug.cgi?id=2523619'
RELEVANT = re.compile(r'openpgpverify|sequoia|\bsqv\b', re.I)
IN_SCOPE = ('macro-simple', 'macro-complex', 'raw-verify')
MINE = 'jjelen'


def load(path):
    return {r['package']: r for r in map(json.loads, open(path))}


def get_json(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=60) as fh:
                return json.load(fh)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            err = e
        except Exception as e:  # network hiccup: retry
            err = e
        time.sleep(2 * (i + 1))
    raise RuntimeError('%s: %r' % (url, err))


def fetch_prs(pkgs):
    def one(pkg):
        d = get_json(PAGURE % pkg) or {}
        return [(pkg, str(p['id']), p['status'], p['user']['name'],
                 'https://src.fedoraproject.org/rpms/%s/pull-request/%s' % (pkg, p['id']),
                 p['title'].replace('\t', ' '),
                 time.strftime('%Y-%m-%d', time.gmtime(int(p.get('closed_at') or
                                                            p['last_updated']))))
                for p in d.get('requests', []) if RELEVANT.search(p['title'])]
    rows = []
    with concurrent.futures.ThreadPoolExecutor(8) as ex:
        for r in ex.map(one, sorted(pkgs)):
            rows += r
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('baseline')
    ap.add_argument('today')
    ap.add_argument('out')
    ap.add_argument('--prs', required=True)
    ap.add_argument('--fetch', action='store_true')
    ap.add_argument('--since', nargs=2, metavar=('INVENTORY', 'PRS'),
                    help='previous report inputs: adds a "changes since" section')
    a = ap.parse_args()
    base, today = load(a.baseline), load(a.today)
    st = state.load()
    start = {p for p, r in base.items() if r['category'] in IN_SCOPE}
    pre = {p for p, r in base.items() if r['category'] == 'converted'}
    # Packages that appeared later with a GnuPG verification count too.
    added = {p for p, r in today.items() if p not in base and r['category'] in IN_SCOPE}
    if a.fetch:
        rows = fetch_prs(start | added | pre)
        with open(a.prs, 'w') as fh:
            fh.write('package\tid\tstatus\tauthor\turl\ttitle\tupdated\n')
            fh.writelines('\t'.join(r) + '\n' for r in rows)
    prs = collections.defaultdict(list)
    for line in list(open(a.prs))[1:]:
        r = dict(zip(('package', 'id', 'status', 'author', 'url', 'title', 'updated'),
                     line.rstrip('\n').split('\t')))
        prs[r['package']].append(r)
    try:
        bugs = get_json(BUGZILLA)['bugs']
    except Exception as e:
        print('bugzilla: %s' % e, file=sys.stderr)
        bugs = None
    pkg_bugs = [b for b in bugs or [] if b['component'] != ['openpgpverify']]

    def pr_state(p):
        s = {r['status'] for r in prs.get(p, [])}
        return 'Merged' if 'Merged' in s else 'Open' if 'Open' in s else \
            'Closed' if s else None

    status = {}
    for p in sorted(start | added):
        t = today.get(p)
        cat = t['category'] if t else None
        ps = pr_state(p)
        mine = any(r['author'] == MINE for r in prs.get(p, []))
        if cat == 'converted':
            how = ('our PR' if ps == 'Merged' and mine else
                   'PR by someone else' if ps == 'Merged' else 'maintainer, no PR')
            status[p] = ('converted', how)
        elif t is None:
            status[p] = ('retired', 'not in the spec snapshot any more')
        elif cat not in IN_SCOPE:
            status[p] = ('dropped', 'no signature verification left (%s)' % cat)
        elif ps == 'Merged':
            status[p] = ('merged', 'PR merged, not in the snapshot yet')
        elif ps == 'Open':
            status[p] = ('open-pr', 'our PR' if mine else 'PR by someone else')
        else:
            s = (st.get(p) or {}).get('status')
            if p in added:
                why = 'new package since 2026-10-06'
            elif s == 'tested':
                why = 'tested, PR ready but not opened' + (' (an earlier PR was closed)'
                                                           if ps == 'Closed' else '')
            elif s == 'regression':
                kr = ((st[p].get('keyring_refresh') or {}).get('status'))
                why = ('signature fails with sqv, keyring refresh awaiting review'
                       if kr in ('proposed', 'approved') else
                       'signature fails with sqv, needs upstream/maintainer action (bug)')
            elif s in ('manual', 'guard-failed', 'not-buildable', 'error'):
                why = 'needs manual work (%s)' % s
            else:
                why = 'not tested (%s)' % (s or 'not in state')
            status[p] = ('todo', why)

    total = len(start)
    by = collections.Counter(v[0] for p, v in status.items() if p in start)
    done = by['converted'] + by['merged']
    how = collections.Counter(v[1] for v in status.values() if v[0] == 'converted')
    todo = collections.Counter(v[1] for v in status.values() if v[0] == 'todo')
    openp = collections.Counter(v[1] for v in status.values() if v[0] == 'open-pr')
    allprs = [r for rs in prs.values() for r in rs]
    prc = collections.Counter((r['author'] == MINE, r['status']) for r in allprs)
    eln = set(open(os.path.join(state.ROOT, 'data', 'eln-in-scope.txt')).read().split())
    eln_by = collections.Counter(status[p][0] for p in eln if p in status)

    def pct(n, d=total):
        return '%d (%d %%)' % (n, round(100.0 * n / d)) if d else str(n)

    snap = os.path.basename(a.today)[len('inventory-'):-len('.jsonl')]
    L = ['# Migration progress as of %s' % time.strftime('%Y-%m-%d'), '',
         'Generated by `scripts/progress.py` from the spec snapshot of %s (`%s`), the '
         'starting snapshot of 2026-10-06 and the dist-git PRs whose title mentions '
         'openpgpverify (Pagure, fetched %s).' % (snap, os.path.basename(a.today),
                                                   time.strftime('%Y-%m-%d %H:%M UTC',
                                                                 time.gmtime())), '',
         '## Summary', '',
         'On 2026-10-06, **%d packages** verified upstream sources with GnuPG '
         '(%d with plain `%%gpgverify`, %d with a more complex `%%gpgverify` use, %d calling '
         '`gpg`/`gpgv` directly). %d more already used `%%openpgpverify`.'
         % (total, sum(base[p]['category'] == 'macro-simple' for p in start),
            sum(base[p]['category'] == 'macro-complex' for p in start),
            sum(base[p]['category'] == 'raw-verify' for p in start), len(pre)), '',
         'That is %d verification calls in total (%d `%%gpgverify`, %d direct GnuPG). Another '
         '%d packages had `BuildRequires: gnupg2` without verifying anything; they are not '
         'counted here.' % (
             sum(len(base[p]['calls']) + len(base[p]['raw_verify']) for p in start),
             sum(len(base[p]['calls']) for p in start),
             sum(len(base[p]['raw_verify']) for p in start),
             sum(r['category'] == 'gnupg2-br-only' for r in base.values())), '',
         '| | Packages | of %d |' % total, '|---|---|---|',
         '| **Converted to `%%openpgpverify`** | **%d** | %d %% |'
         % (done, round(100.0 * done / total)),
         '| &nbsp;&nbsp;in the snapshot | %d | |' % by['converted'],
         '| &nbsp;&nbsp;PR merged after the snapshot | %d | |' % by['merged'],
         '| **PR open** | **%d** | %d %% |' % (by['open-pr'],
                                              round(100.0 * by['open-pr'] / total)),
         '| Retired | %d | |' % by['retired'],
         '| Signature check dropped by the maintainer | %d | |' % by['dropped'],
         '| **Still to do** | **%d** | %d %% |' % (by['todo'],
                                                 round(100.0 * by['todo'] / total)),
         '']
    if added:
        L += ['Not counted above: %d package(s) added since with `%%gpgverify` (%s).'
              % (len(added), ', '.join(sorted(added))), '']
    L += ['### How the converted ones got there', '',
          '| | Packages |', '|---|---|']
    L += ['| %s | %d |' % (k, v) for k, v in how.most_common()]
    L += ['', '### Open PRs', '', '| | Packages |', '|---|---|']
    L += ['| %s | %d |' % (k, v) for k, v in openp.most_common()]
    L += ['', '### Still to do', '', '| | Packages |', '|---|---|']
    L += ['| %s | %d |' % (k, v) for k, v in todo.most_common()]
    L += ['', '### PRs (all packages)', '',
          '| Author | Open | Merged | Closed |', '|---|---|---|---|']
    for mine, name in ((True, MINE), (False, 'others')):
        L.append('| %s | %d | %d | %d |' % (name, prc[(mine, 'Open')],
                                             prc[(mine, 'Merged')], prc[(mine, 'Closed')]))
    L += ['', '### ELN (%d packages, [eln#610](https://github.com/fedora-eln/eln/issues/610))'
          % len(eln), '', '| | Packages |', '|---|---|']
    L += ['| %s | %d |' % (k, eln_by[k]) for k in
          ('converted', 'merged', 'open-pr', 'todo', 'retired', 'dropped') if eln_by[k]]
    L += ['', '### Bugs', '']
    if bugs is None:
        L.append('Bugzilla could not be queried.')
    else:
        L.append('[rhbz#2523619](%s) has %d package bug(s) blocking it%s' % (
            TRACKER, len(pkg_bugs), (': ' + ', '.join(
                '[%s](https://bugzilla.redhat.com/%d) %s' % (b['component'][0], b['id'],
                                                            b['status'])
                for b in pkg_bugs)) if pkg_bugs else '.'))
    if a.since:
        old = load(a.since[0])
        oldprs = {(r[0], r[1]): r for r in (l.rstrip('\n').split('\t')
                                            for l in list(open(a.since[1]))[1:])}
        newc = sorted(p for p, v in status.items() if v[0] == 'converted' and
                      (old.get(p) or {}).get('category') != 'converted')
        when = os.path.basename(a.since[0])[len('inventory-'):-len('.jsonl')]
        L += ['', '### Changes since %s' % when, '',
              'Converted since then (%d): %s' % (len(newc), ', '.join(
                  '%s (%s)' % (p, status[p][1]) for p in newc) or '-'), '']
        rows = []
        for k, rs in sorted((k, r) for k, r in
                            ((('%s#%s' % (r['package'], r['id'])), r)
                             for rs in prs.values() for r in rs)):
            o = oldprs.get((rs['package'], rs['id']))
            if not o:
                rows.append('| %s | %s | new, %s |' % (k, rs['author'], rs['status'].lower()))
            elif o[2] != rs['status']:
                rows.append('| %s | %s | %s → %s |' % (k, rs['author'], o[2].lower(),
                                                      rs['status'].lower()))
        if rows:
            L += ['| PR | Author | Change |', '|---|---|---|'] + rows
    L += ['', '## Per package', '',
          'Only packages not converted yet.', '',
          '| Package | Status | Detail | PR |', '|---|---|---|---|']
    for p in sorted(status):
        s, why = status[p]
        if s == 'converted':
            continue
        links = ', '.join('[#%s](%s) %s' % (r['id'], r['url'], r['status'].lower())
                          for r in prs.get(p, []))
        L.append('| %s | %s | %s | %s |' % (p, s, why, links))
    with open(a.out, 'w') as fh:
        fh.write('\n'.join(L) + '\n')
    print('start %d: converted %d, merged %d, open PR %d, retired %d, dropped %d, todo %d'
          % (total, by['converted'], by['merged'], by['open-pr'], by['retired'],
             by['dropped'], by['todo']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
