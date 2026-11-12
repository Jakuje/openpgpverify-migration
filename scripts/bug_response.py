"""Record what came back on a package's bug, so that patterns (dead upstreams,
maintainers who decline) stay visible in reports/bug-groups-*.md.

Usage: bug_response.py PKG KIND --note TEXT [--comment N]
       bug_response.py --list

KIND is one of KINDS. The latest response replaces the earlier one; the
earlier ones are kept in bug_response_history.
"""
import argparse, datetime, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import state  # noqa: E402

KINDS = {
    'upstream-fixed': 'upstream fixed the key or signature',
    'raised-upstream': 'the maintainer raised it upstream',
    'upstream-silent': 'upstream does not answer',
    'upstream-dead': 'upstream unmaintained',
    'declined': 'the maintainer will not pursue it',
    'other': 'other',
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('package', nargs='?')
    ap.add_argument('kind', nargs='?', choices=sorted(KINDS))
    ap.add_argument('--note', help='one line: what was said, in our words')
    ap.add_argument('--comment', type=int, help='comment number on the bug')
    ap.add_argument('--list', action='store_true')
    a = ap.parse_args()
    st = state.load()
    if a.list:
        for p, s in sorted(st.items()):
            r = s.get('bug_response')
            if r:
                print('%-24s %-16s %s %s' % (p, r['kind'], r['date'], r['note']))
        return
    if not (a.package and a.kind and a.note):
        ap.error('needs PKG KIND --note')
    s = st[a.package]
    if not s.get('bug_id'):
        sys.exit('%s has no bug' % a.package)
    if s.get('bug_response'):
        s.setdefault('bug_response_history', []).append(s['bug_response'])
    s['bug_response'] = dict(kind=a.kind, note=a.note, comment=a.comment,
                             date=datetime.date.today().isoformat())
    s['updated'] = state.now()
    state.save(st)
    print('%s: %s' % (a.package, a.kind))


if __name__ == '__main__':
    main()
