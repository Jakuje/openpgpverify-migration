#!/usr/bin/python3 -I
"""Create or refresh data/state/packages.jsonl from an inventory.

Usage: seed_state.py INVENTORY.jsonl OWNERS.json

INVENTORY.jsonl  output of classify.py
OWNERS.json      https://src.fedoraproject.org/extras/pagure_owner_alias.json

Adds a record (status "inventory") for each new in-scope package and
refreshes the inventory-derived fields of existing ones. Results and status
from later phases are kept. Packages that dropped out of scope are marked
"skipped" rather than removed.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import state  # noqa: E402

# Fields copied from the inventory; everything else belongs to later phases.
INVENTORY_FIELDS = ('category', 'forms', 'conditional', 'rhel_conditional',
                    'gnupg2_action', 'autochangelog', 'srpm_size')


def main():
    inv = state.load_inventory(sys.argv[1])
    with open(sys.argv[2]) as fh:
        owners = json.load(fh)['rpms']
    st = state.load()
    added = updated = dropped = 0
    for name, rec in inv.items():
        if not rec['in_scope']:
            continue
        s = st.get(name)
        if s is None:
            s = st[name] = dict(package=name, status='inventory', results=[],
                                pr_url=None, bug_id=None, existing_prs=None,
                                announced=None, nag_sent=None, escalated=None)
            added += 1
        else:
            updated += 1
        for f in INVENTORY_FIELDS:
            s[f] = rec.get(f)
        s['inventory_calls'] = len(rec['calls']) + len(rec['raw_verify'])
        s['eln_relevant'] = rec['mentions_rhel']
        s['maintainers'] = owners.get(name, [])
        s['updated'] = state.now()
    for name, s in st.items():
        if name not in inv or not inv[name]['in_scope']:
            if s['status'] != 'skipped':
                s['status'] = 'skipped'
                s['skip_reason'] = 'no longer in scope per inventory'
                s['updated'] = state.now()
                dropped += 1
    state.save(st)
    print('added %d, refreshed %d, newly skipped %d, total %d'
          % (added, updated, dropped, len(st)))


if __name__ == '__main__':
    main()
