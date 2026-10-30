#!/usr/bin/python3 -I
"""List packages whose PR can be opened now, with the commands to do it.

Usage: ready_list.py PKGLIST OUT.md

A package is ready when Phase 1 passed (status `tested`), no keyring refresh
is involved, nobody else has an open PR, and the rawhide branch in dist-git
is still at the commit that was tested (checked live with git ls-remote).

All are the same kind of change: rename + BuildRequires (+ Release bump for
specs without rpmautospec). "%{?rhel}" marks specs with RHEL conditionals,
whose PR text mentions that openpgpverify is not in EPEL 8.
"""
import concurrent.futures
import glob
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import phase1  # noqa: E402
import render_proposals  # noqa: E402
import state  # noqa: E402

REPO = 'https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/'


def head(pkg):
    for _ in range(3):
        try:
            p = subprocess.run(['git', 'ls-remote', phase1.DISTGIT % pkg, 'refs/heads/rawhide'],
                               capture_output=True, text=True, timeout=60)
        except subprocess.TimeoutExpired:
            continue
        if p.returncode == 0:
            return p.stdout.split('\t')[0]
    return None


def diffstat(pkg):
    found = glob.glob(os.path.join(render_proposals.OUT, pkg,
                                   '*-Verify-source-signatures-with-openpgpverify.patch'))
    if not found:
        return None
    patch = found[0]
    t = open(patch).read().split('\n---\n', 1)[-1]
    m = re.search(r'(\d+) insertions?\(\+\)(?:, (\d+) deletions?)?', t)
    return '+%s/-%s' % (m.group(1), m.group(2) or 0) if m else '?'


def main():
    pkgs = [l.strip() for l in open(sys.argv[1]) if l.strip()]
    st = state.load()
    rows = []
    stale, other = [], []
    pkgs = [p for p in sorted(set(pkgs)) if st.get(p) and st[p].get('status') == 'tested'
            and not st[p].get('existing_prs') and not st[p].get('keyring_refresh_applied')]
    with concurrent.futures.ThreadPoolExecutor(8) as ex:
        heads = dict(zip(pkgs, ex.map(head, pkgs)))
    for p in pkgs:
        s = st[p]
        if heads[p] != s.get('spec_commit'):
            stale.append(p)
            continue
        ds = diffstat(p)
        if ds is None:
            other.append(p)
            continue
        rows.append((p, ' '.join(s.get('maintainers', [])), ds,
                     'yes' if s.get('release_bumped') else '',
                     'yes' if s.get('rhel_conditional') else '',
                     {'drop': 'dropped (checked)', 'keep': 'kept'}.get(
                         (s.get('gnupg2_check') or {}).get('verdict'), ''),
                     (s.get('tested_at') or '?')[:10]))
    out = ['# PRs ready to open', '',
           'Generated %s by `scripts/ready_list.py` from `%s`. Every package below passed '
           'Phase 1 (`%%prep` with `%%gpgverify` and `%%openpgpverify` in mock, all '
           'verification calls logged), has no open PR, and its rawhide branch is still at '
           'the tested commit (checked when this list was generated).'
           % (state.now(), sys.argv[1]), '']
    out += ['## Ready (%d)' % len(rows), '',
            '| Package | Maintainers | Diff | Release bump | `%{?rhel}` | BR gnupg2 | Tested |',
            '|---|---|---|---|---|---|---|']
    out += ['| [%s](%s%s/) | %s | %s | %s | %s | %s | %s |' % (p, REPO, p, m, ds, rb, rh, gn, t)
            for p, m, ds, rb, rh, gn, t in rows]
    out.append('')
    if stale:
        out += ['Not listed because dist-git moved since the test (re-run `phase1.py`): ' +
                ', '.join(stale), '']
    if other:
        out += ['Not listed because no proposal is rendered yet: ' + ', '.join(other), '']
    out += ['## Opening a PR', '',
            'The patch is the complete commit (author, message with the `Assisted-by:` '
            'trailer); `PR.md` has the title and description.', '',
            '```sh',
            'P=libmnl   # package',
            'fedpkg clone "$P" && cd "$P"',
            'git am ~/devel/openpgpverify-migration/proposals/"$P"/*.patch',
            'fedpkg fork                      # adds a remote named after your FAS user',
            'git push "$USER" HEAD:openpgpverify',
            '# then open the PR from the fork (branch openpgpverify -> rawhide) in the web UI,',
            '# pasting title and description from proposals/$P/PR.md',
            '```', '']
    open(sys.argv[2], 'w').write('\n'.join(out))
    print('ready %d, stale %d, not rendered %d' % (len(rows), len(stale), len(other)))


if __name__ == '__main__':
    main()
