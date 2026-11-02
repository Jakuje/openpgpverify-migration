#!/usr/bin/python3 -I
"""Open the rendered PRs in dist-git, one batch at a time.

Usage: open_prs.py check   PKG...   dist-git still at the tested commit, no PR yet
       open_prs.py prepare PKG...   clone, apply proposals/PKG/*.patch (local only)
       open_prs.py open    PKG...   fork, push the branch to the fork, open the PR

Guards, so a push can only ever reach the fork:
- the clone's "origin" push URL is set to an invalid value;
- a pre-push hook rejects any URL but FORK_URL and any ref but BRANCH,
  and refuses branch deletion;
- pushes never use --force; if the fork already has a different BRANCH,
  the package is skipped.

`open` needs a Pagure API token (ACLs fork_project, pull_request_create)
in ~/.config/rpkg/fedpkg.conf ([fedpkg.distgit] token = ...) and an
SSH key registered in FAS for the push. The token is never printed.
"""
import configparser
import glob
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import state  # noqa: E402

FORK_USER = 'jjelen'
BRANCH = 'openpgpverify'
API = 'https://src.fedoraproject.org/api/0'
ANON_URL = 'https://src.fedoraproject.org/rpms/%s.git'
FORK_URL = 'ssh://%s@pkgs.fedoraproject.org/forks/%s/rpms/%%s.git' % (FORK_USER, FORK_USER)
PR_WORDS = ('openpgpverify', 'sequoia', 'sqv')

PRE_PUSH = r'''#!/bin/sh
# Installed by open_prs.py: only BRANCH may be pushed, and only to the fork.
url="$2"
[ "$url" = "FORK_URL" ] || { echo "pre-push: refusing to push to $url" >&2; exit 1; }
while read -r lref lsha rref rsha; do
    [ "$rref" = "refs/heads/BRANCH" ] || { echo "pre-push: refusing ref $rref" >&2; exit 1; }
    case "$lsha" in *[!0]*) ;; *) echo "pre-push: refusing deletion" >&2; exit 1;; esac
done
exit 0
'''


def git(d, *args, check=True):
    return subprocess.run(['git', '-C', d] + list(args), capture_output=True, text=True,
                          check=check, timeout=600)


def api(path, data=None, token=None):
    req = urllib.request.Request(API + path, data=urllib.parse.urlencode(data).encode()
                                 if data is not None else None)
    if token:
        req.add_header('Authorization', 'token ' + token)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.load(e)
        except ValueError:
            return e.code, {}


def token():
    c = configparser.ConfigParser()
    c.read(os.path.expanduser('~/.config/rpkg/fedpkg.conf'))
    t = c.get('fedpkg.distgit', 'token', fallback='').strip()
    if not t:
        sys.exit('no token in ~/.config/rpkg/fedpkg.conf [fedpkg.distgit]')
    return t


def check(pkg, rec):
    """Problems that block the PR; empty when it can be opened."""
    probs = []
    if not glob.glob(os.path.join(state.ROOT, 'proposals', pkg, '*.patch')):
        probs.append('no rendered patches')
    if rec.get('pr_url'):
        probs.append('PR already recorded: %s' % rec['pr_url'])
    r = subprocess.run(['git', 'ls-remote', ANON_URL % pkg, 'refs/heads/rawhide'],
                       capture_output=True, text=True, timeout=120)
    head = r.stdout.split()[0] if r.returncode == 0 and r.stdout else None
    if head != rec.get('spec_commit'):
        probs.append('rawhide at %s, tested %s' % (head and head[:12], rec.get('spec_commit', '')[:12]))
    code, d = api('/rpms/%s/pull-requests?status=all&per_page=100' % pkg)
    if code != 200:
        probs.append('PR list: HTTP %s' % code)
    for p in d.get('requests', []):
        text = (p['title'] + ' ' + (p.get('initial_comment') or '')).lower()
        if any(w in text for w in PR_WORDS) and p['status'] != 'Closed':
            probs.append('existing PR #%d (%s, %s)' % (p['id'], p['status'], p['user']['name']))
    return probs


def prepare(pkg, rec):
    d = os.path.join(state.ROOT, 'work', pkg, 'pr-git')
    subprocess.run(['rm', '-rf', d], check=True)
    subprocess.run(['git', 'clone', '-q', '--branch', 'rawhide', ANON_URL % pkg, d],
                   check=True, timeout=1200)
    head = git(d, 'rev-parse', 'HEAD').stdout.strip()
    if head != rec['spec_commit']:
        return 'rawhide moved to %s' % head[:12]
    git(d, 'checkout', '-q', '-b', BRANCH)
    patches = sorted(glob.glob(os.path.join(state.ROOT, 'proposals', pkg, '*.patch')))
    r = git(d, 'am', '-q', *patches, check=False)
    if r.returncode:
        git(d, 'am', '--abort', check=False)
        return 'git am failed: %s' % r.stderr.strip()[:200]
    git(d, 'remote', 'set-url', '--push', 'origin', 'no-push-to-origin')
    git(d, 'remote', 'add', 'fork', FORK_URL % pkg)
    hook = os.path.join(d, '.git', 'hooks', 'pre-push')
    with open(hook, 'w') as fh:
        fh.write(PRE_PUSH.replace('FORK_URL', FORK_URL % pkg).replace('BRANCH', BRANCH))
    os.chmod(hook, 0o755)
    n = git(d, 'rev-list', '--count', 'origin/rawhide..HEAD').stdout.strip()
    return 'ready: %s commit(s) on %s' % (n, BRANCH)


def open_pr(pkg, rec, tok):
    d = os.path.join(state.ROOT, 'work', pkg, 'pr-git')
    if not os.path.isdir(os.path.join(d, '.git')):
        return 'not prepared'
    if git(d, 'merge-base', 'HEAD', 'origin/rawhide').stdout.strip() != rec['spec_commit']:
        return 'branch is not based on the tested commit'
    code, _ = api('/fork/%s/rpms/%s' % (FORK_USER, pkg))
    if code == 404:
        code, out = api('/fork', dict(repo=pkg, namespace='rpms', wait='true'), tok)
        if code != 200:
            return 'fork failed: HTTP %s %s' % (code, out.get('error', ''))
    elif code != 200:
        return 'fork lookup: HTTP %s' % code
    r = git(d, 'ls-remote', 'fork', 'refs/heads/' + BRANCH, check=False)
    remote = r.stdout.split()[0] if r.stdout else None
    local = git(d, 'rev-parse', 'HEAD').stdout.strip()
    if remote and remote != local:
        return 'fork already has a different %s (%s); not overwriting' % (BRANCH, remote[:12])
    if not remote:
        r = git(d, 'push', 'fork',
                '%s:refs/heads/%s' % (BRANCH, BRANCH), check=False)
        if r.returncode:
            return 'push failed: %s' % r.stderr.strip()[-300:]
    text = open(os.path.join(state.ROOT, 'proposals', pkg, 'PR.md')).read()
    title, _, body = text.partition('\n')
    code, out = api('/rpms/%s/pull-request/new' % pkg, dict(
        title=title.lstrip('# ').strip(), initial_comment=body.strip(),
        branch_to='rawhide', branch_from=BRANCH, repo_from=pkg,
        repo_from_namespace='rpms', repo_from_username=FORK_USER), tok)
    if code != 200:
        return 'PR failed: HTTP %s %s' % (code, out.get('error', ''))
    url = 'https://src.fedoraproject.org/rpms/%s/pull-request/%d' % (pkg, out['id'])
    rec['pr_url'] = url
    rec['updated'] = state.now()
    return url


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ('check', 'prepare', 'open'):
        sys.exit(__doc__)
    cmd, pkgs = sys.argv[1], sys.argv[2:]
    st = state.load()
    tok = token() if cmd == 'open' else None
    for pkg in pkgs:
        rec = st.get(pkg)
        if rec is None:
            print('%-40s not in state' % pkg)
            continue
        probs = check(pkg, rec)
        if probs:
            print('%-40s SKIP: %s' % (pkg, '; '.join(probs)))
            continue
        if cmd == 'check':
            print('%-40s ok' % pkg)
        elif cmd == 'prepare':
            print('%-40s %s' % (pkg, prepare(pkg, rec)))
        else:
            print('%-40s %s' % (pkg, open_pr(pkg, rec, tok)))
            state.save(st)


if __name__ == '__main__':
    main()
