#!/usr/bin/python3 -I
"""List packages whose PR can be opened now, with the commands to do it.

Usage: ready_list.py PKGLIST OUT.md

A package is ready when Phase 1 passed (status `tested`), no keyring refresh
is involved, nobody else has an open PR, and the rawhide branch in dist-git
is still at the commit that was tested (checked live with git ls-remote).

  trivial   rename + BuildRequires (+ Release bump for non-rpmautospec specs)
  template  also wraps the check in %if for EPEL (spec has %{?rhel} conditionals)
"""
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
    p = subprocess.run(['git', 'ls-remote', phase1.DISTGIT % pkg, 'refs/heads/rawhide'],
                       capture_output=True, text=True, timeout=60)
    return p.stdout.split('\t')[0] if p.returncode == 0 else None


def diffstat(pkg):
    patch = os.path.join(render_proposals.OUT, pkg, render_proposals.PATCH_NAME)
    if not os.path.exists(patch):
        return None
    t = open(patch).read().split('\n---\n', 1)[-1]
    m = re.search(r'(\d+) insertions?\(\+\)(?:, (\d+) deletions?)?', t)
    return '+%s/-%s' % (m.group(1), m.group(2) or 0) if m else '?'


def main():
    pkgs = [l.strip() for l in open(sys.argv[1]) if l.strip()]
    st = state.load()
    rows = {'trivial': [], 'template': []}
    stale, other = [], []
    for p in sorted(set(pkgs)):
        s = st.get(p)
        if not s or s.get('status') != 'tested' or s.get('existing_prs') or \
                s.get('keyring_refresh_applied'):
            continue
        if head(p) != s.get('spec_commit'):
            stale.append(p)
            continue
        ds = diffstat(p)
        if ds is None:
            other.append(p)
            continue
        kind = 'template' if s.get('rhel_conditional') else 'trivial'
        rows[kind].append((p, ' '.join(s.get('maintainers', [])), ds,
                           'yes' if s.get('release_bumped') else '',
                           (s.get('tested_at') or '?')[:10]))
    out = ['# PRs ready to open', '',
           'Generated %s by `scripts/ready_list.py` from `%s`. Every package below passed '
           'Phase 1 (`%%prep` with `%%gpgverify` and `%%openpgpverify` in mock, all '
           'verification calls logged), has no open PR, and its rawhide branch is still at '
           'the tested commit (checked when this list was generated).'
           % (state.now(), sys.argv[1]), '']
    titles = {'trivial': 'Trivial: rename + BuildRequires', 'template':
              'Tested, with the EPEL-compatible `%if` template (bigger diff)'}
    for kind in ('trivial', 'template'):
        out += ['## %s (%d)' % (titles[kind], len(rows[kind])), '',
                '| Package | Maintainers | Diff | Release bump | Tested |', '|---|---|---|---|---|']
        out += ['| [%s](%s%s/) | %s | %s | %s | %s |' % (p, REPO, p, m, ds, rb, t)
                for p, m, ds, rb, t in rows[kind]]
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
            'git am ~/devel/openpgpverify-migration/proposals/"$P"/0001-*.patch',
            'fedpkg fork                      # adds a remote named after your FAS user',
            'git push "$USER" HEAD:openpgpverify',
            '# then open the PR from the fork (branch openpgpverify -> rawhide) in the web UI,',
            '# pasting title and description from proposals/$P/PR.md',
            '```', '']
    open(sys.argv[2], 'w').write('\n'.join(out))
    print('trivial %d, template %d, stale %d, not rendered %d'
          % (len(rows['trivial']), len(rows['template']), len(stale), len(other)))


if __name__ == '__main__':
    main()
