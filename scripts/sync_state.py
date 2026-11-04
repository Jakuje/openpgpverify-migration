#!/usr/bin/python3 -I
"""Bring data/state/packages.jsonl in line with today's spec dump and PR list,
so packages converted or PR'd outside our scripts stop showing up as to do.

Usage: sync_state.py INVENTORY.jsonl PRS.tsv [--write]

INVENTORY.jsonl  today's inventory (classify.py)
PRS.tsv          today's PR list (progress.py --fetch)
--write          save the changes; without it, only print them

- Our PR (author jjelen, not closed) and no pr_url recorded: pr_url is set.
- Someone else's PR (not closed): added to existing_prs.
- Converted in rawhide while state has no PR of ours: status superseded,
  like a Phase 1 re-run would set it.
Every package gets rawhide_category (today's classify.py category).
"""
import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import phase1  # noqa: E402
import progress  # noqa: E402
import state  # noqa: E402

LIVE = ('regression', 'tested', 'inventory', 'not-buildable', 'both-fail', 'still-fails')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('inventory')
    ap.add_argument('prs')
    ap.add_argument('--write', action='store_true')
    a = ap.parse_args()
    inv = state.load_inventory(a.inventory)
    prs = {}
    for r in csv.DictReader(open(a.prs), delimiter='\t'):
        if r['status'] != 'Closed':
            prs.setdefault(r['package'], []).append(r)
    day = os.path.basename(a.inventory).rsplit('-', 3)[-3:]
    day = '-'.join(day).split('.')[0]
    with phase1.LOCK:
        st = state.load()
        changes = []
        for pkg, r in sorted(st.items()):
            cat = inv.get(pkg, {}).get('category')
            r['rawhide_category'] = cat
            for p in sorted(prs.get(pkg, []), key=lambda x: (x['status'] != 'Open', x['updated'])):
                if p['author'] == progress.MINE:
                    if not r.get('pr_url'):
                        r['pr_url'] = p['url']
                        changes.append('%-26s pr_url %s (%s)' % (pkg, p['url'], p['status']))
                elif p['url'] not in (r.get('existing_prs') or []):
                    r['existing_prs'] = (r.get('existing_prs') or []) + [p['url']]
                    changes.append('%-26s existing_prs + %s (%s, %s)'
                                   % (pkg, p['url'], p['author'], p['status']))
            if cat == 'converted' and not r.get('pr_url') and r.get('status') in LIVE:
                changes.append('%-26s %s -> superseded (converted in rawhide)'
                               % (pkg, r['status']))
                r['status'] = 'superseded'
                r['outcome_detail'] = 'converted in rawhide (inventory %s)' % day
        print('\n'.join(changes) or 'nothing to sync')
        if a.write:
            state.save(st)
    return 0


if __name__ == '__main__':
    sys.exit(main())
