#!/usr/bin/python3 -I
"""Summarize data/state/packages.jsonl as Markdown.

Usage: report.py [OUT.md] [--only PKGLIST]

PKGLIST  file with one package per line; limits the per-package table
         (e.g. data/pilot.txt). Totals always cover all tested packages.
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import state  # noqa: E402


def cell(s, n=110):
    s = (s or '').replace('|', '\\|').replace('\n', ' ')
    return s if len(s) <= n else s[:n - 1] + '…'


def main():
    args = sys.argv[1:]
    only = None
    if '--only' in args:
        i = args.index('--only')
        only = [l.strip() for l in open(args[i + 1]) if l.strip()]
        del args[i:i + 2]
    out = args[0] if args else None
    st = state.load()
    tested = [s for s in st.values() if s.get('harness_version')]
    lines = ['# Phase 1 results', '',
             'Generated %s from `data/state/packages.jsonl`: %d of %d packages tested.'
             % (state.now(), len(tested), len(st)), '']
    lines += ['| Status | Packages |', '|---|---|']
    for k, v in collections.Counter(s['status'] for s in tested).most_common():
        lines.append('| `%s` | %d |' % (k, v))
    reasons = collections.Counter(r.get('failure_reason') for s in tested
                                  for r in s.get('results', []) if r.get('failure_reason'))
    if reasons:
        lines += ['', '| Regression reason | Calls |', '|---|---|']
        lines += ['| `%s` | %d |' % kv for kv in reasons.most_common()]
    rows = [st[p] for p in only if p in st] if only else sorted(tested, key=lambda s: s['package'])
    lines += ['', '| Package | Status | Calls old→new | Chroots | Notes |', '|---|---|---|---|---|']
    for s in rows:
        chroots = ', '.join('%s: %s' % (r['chroot'].replace('fedora-', '').replace('-x86_64', ''),
                                        r.get('outcome')) for r in s.get('results', []))
        notes = '; '.join([r['detail'] for r in s.get('results', []) if r.get('detail')] +
                          (s.get('convert_notes') or []) +
                          ['reason: %s' % r['failure_reason'] for r in s.get('results', [])
                           if r.get('failure_reason')] +
                          (['keyring refresh: %s' % s['keyring_refresh']['status']]
                           if s.get('keyring_refresh') else []))
        lines.append('| %s | `%s` | %s→%s | %s | %s |' % (
            s['package'], s.get('status'), s.get('expanded_calls_old', '-'),
            s.get('expanded_calls_new', '-'), chroots, cell(notes)))
    text = '\n'.join(lines) + '\n'
    if out:
        with open(out, 'w') as fh:
            fh.write(text)
    else:
        sys.stdout.write(text)


if __name__ == '__main__':
    main()
