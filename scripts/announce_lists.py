#!/usr/bin/python3 -I
"""Package lists for the devel-announce mail (FESCo mass package change policy).

Usage: announce_lists.py OWNERS.json [OUTDIR]

OWNERS.json  https://src.fedoraproject.org/extras/pagure_owner_alias.json
OUTDIR       default: announce/

Writes packages-by-name.txt (package: maintainers) and
packages-by-maintainer.txt (maintainer: packages) for the packages that still
use %gpgverify or gpg directly, i.e. not already converted, retired or skipped.
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import state  # noqa: E402

DONE = {'superseded', 'skipped'}


def main():
    owners = json.load(open(sys.argv[1]))['rpms']
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(state.ROOT, 'announce')
    os.makedirs(out, exist_ok=True)
    pkgs = sorted(p for p, r in state.load().items() if r.get('status') not in DONE)
    by_maint = collections.defaultdict(list)
    width = max(len(p) for p in pkgs)
    with open(os.path.join(out, 'packages-by-name.txt'), 'w') as fh:
        for p in pkgs:
            m = sorted(owners.get(p, []))
            fh.write('%-*s  %s\n' % (width, p, ' '.join(m)))
            for x in m:
                by_maint[x].append(p)
    width = max(len(m) for m in by_maint)
    with open(os.path.join(out, 'packages-by-maintainer.txt'), 'w') as fh:
        for m in sorted(by_maint, key=str.lower):
            fh.write('%-*s  %s\n' % (width, m, ' '.join(by_maint[m])))
    print('%d packages, %d maintainers' % (len(pkgs), len(by_maint)))


if __name__ == '__main__':
    main()
