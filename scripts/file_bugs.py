"""File the rendered bug drafts (proposals/PKG/BUG.md) in Bugzilla.

Usage: file_bugs.py --tracker ID PKG...          dry run: print what would be sent
       file_bugs.py --tracker ID --file PKG...   create the bugs, record bug_id

Each bug blocks --tracker (an open tracking bug). The API key comes from
~/.config/python-bugzilla/bugzillarc ([bugzilla.redhat.com] api_key = ...) and is
never printed. Bugzilla shows comments as plain text, so the Markdown of BUG.md is
turned into plain text first.

Guards, so nothing is filed twice or against a moved spec:
- the package has no bug_id in the state yet, and its status is still regression;
- no open bug in the component mentions openpgpverify, sqv or Sequoia;
- rawhide dist-git is still at the commit the draft names (--allow-moved to skip,
  e.g. for unrelated spec changes that were checked by hand).
"""
import argparse, datetime, os, re, subprocess, sys

import bugzilla

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import state  # noqa: E402

URL = 'bugzilla.redhat.com'
OPEN = ['NEW', 'ASSIGNED', 'POST', 'MODIFIED', 'ON_QA']
DUP_WORDS = ('openpgpverify', 'sqv', 'sequoia')


def parse(path):
    """Header fields and body of a BUG.md."""
    head, _, body = open(path).read().partition('\n---\n')
    fields = dict(l.split(': ', 1) for l in head.strip().split('\n'))
    return fields, body.strip()


def plain(md):
    """BUG.md Markdown as plain text for Bugzilla."""
    out, code = [], False
    for l in md.split('\n'):
        if l.startswith('```'):
            code = not code
            continue
        if code:
            out.append('    ' + l)
            continue
        l = re.sub(r'^### (.*)$', r'\1:', l)
        l = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'\1 (\2)', l)
        l = re.sub(r'`([^`]+)`', r'\1', l)
        out.append(l)
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(out)).strip() + '\n'


def head_commit(pkg):
    r = subprocess.run(['git', 'ls-remote', 'https://src.fedoraproject.org/rpms/%s.git' % pkg,
                        'refs/heads/rawhide'], capture_output=True, text=True, timeout=60)
    return r.stdout.split()[0] if r.returncode == 0 and r.stdout else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tracker', type=int, required=True, help='open tracking bug to block')
    ap.add_argument('--file', action='store_true', help='really create the bugs')
    ap.add_argument('--allow-moved', action='store_true',
                    help='file even if rawhide dist-git moved past the tested commit')
    ap.add_argument('packages', nargs='+')
    a = ap.parse_args()

    bz = bugzilla.Bugzilla(URL)
    if not bz.logged_in:
        sys.exit('not logged in: put api_key into ~/.config/python-bugzilla/bugzillarc')
    t = bz.getbug(a.tracker, include_fields=['id', 'status', 'summary'])
    if t.status not in OPEN:
        if a.file:
            sys.exit('tracker %d is %s, not open' % (t.id, t.status))
        print('warning: tracker %d is %s; fine for a dry run only' % (t.id, t.status))
    print('tracker: %d %s' % (t.id, t.summary))

    st = state.load()
    for pkg in a.packages:
        s = st.get(pkg) or {}
        path = os.path.join(state.ROOT, 'proposals', pkg, 'BUG.md')
        if s.get('bug_id'):
            print('%-24s skipped: already filed as %s' % (pkg, s['bug_id']))
            continue
        if s.get('status') != 'regression' or not os.path.exists(path):
            print('%-24s skipped: no bug draft (status %s)' % (pkg, s.get('status')))
            continue
        fields, body = parse(path)
        commit = re.search(r'dist-git commit `(\w+)`', body).group(1)
        head = head_commit(pkg)
        if not head:
            print('%-24s skipped: cannot read rawhide head' % pkg)
            continue
        if not head.startswith(commit) and not a.allow_moved:
            print('%-24s skipped: rawhide moved (%s -> %s); re-run phase1 first'
                  % (pkg, commit, head[:12]))
            continue
        q = bz.build_query(product='Fedora', component=pkg, status=OPEN,
                           include_fields=['id', 'summary'])
        dups = [b for b in bz.query(q) if any(w in b.summary.lower() for w in DUP_WORDS)]
        if dups:
            print('%-24s skipped: open bug(s) %s' % (
                pkg, ', '.join('%d (%s)' % (b.id, b.summary) for b in dups)))
            continue
        text = plain(body)
        if not a.file:
            print('=' * 78)
            print('Product: %s | Component: %s | Version: %s | Blocks: %d'
                  % (fields['Product'], fields['Component'], fields['Version'], a.tracker))
            print('Summary: %s\n' % fields['Summary'])
            print(text)
            continue
        cb = bz.build_createbug(product=fields['Product'], component=fields['Component'],
                                version=fields['Version'], summary=fields['Summary'],
                                description=text, blocks=[a.tracker])
        b = bz.createbug(cb)
        s['bug_id'] = b.id
        s['bug_filed'] = datetime.date.today().isoformat()
        state.save(st)          # after every bug, so a failure later loses nothing
        print('%-24s https://%s/show_bug.cgi?id=%d' % (pkg, URL, b.id))


if __name__ == '__main__':
    main()
