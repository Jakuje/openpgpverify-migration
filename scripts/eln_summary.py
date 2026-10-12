#!/usr/bin/python3 -I
"""Draft a status comment for https://github.com/fedora-eln/eln/issues/610.

Usage: eln_summary.py ELN_IN_SCOPE ISSUE_PACKAGES [OUT.md]

ELN_IN_SCOPE    our in-scope packages that are in ELN (one per line)
ISSUE_PACKAGES  the packages listed in the issue (one per line)

Groups the ELN packages by what happens next (PR ready, keyring refresh
waiting for review, bug, manual, converted, someone else's PR) from
data/state/packages.jsonl, and groups the failures by signing key. Nothing
is posted; the output is for the user to edit and post.
"""
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import state  # noqa: E402

REPO = 'https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/'
REASON_TEXT = {
    'sha1-cert': 'SHA-1 self-signatures on the key',
    'sha1-sig': 'SHA-1 release signature',
    'expired': 'key expired before the signature (outdated keyring)',
    'binding-after-signature': 'keyring lacks older self-signatures',
    'weak-key': 'DSA key',
    'unparseable-cert': 'keyring contains a key sqv cannot read (old v3 key)',
    'v3-sig': 'v3 signature',
    'keybox': 'GnuPG keybox keyring',
}


def lines(path):
    return [l.strip() for l in open(path) if l.strip()]


def plist(pkgs, link=False):
    if not pkgs:
        return '(none)'
    return ', '.join(('[%s](%s%s/)' % (p, REPO, p)) if link else p for p in sorted(pkgs))


def main():
    eln, issue = set(lines(sys.argv[1])), set(lines(sys.argv[2]))
    out = sys.argv[3] if len(sys.argv) > 3 else None
    st = state.load()
    groups = collections.defaultdict(list)
    reasons = collections.defaultdict(list)
    keys = collections.defaultdict(list)
    for p in sorted(eln):
        s = st.get(p, {})
        kr = (s.get('keyring_refresh') or {}).get('status')
        res = (s.get('results') or [{}])[0]
        if s.get('existing_prs'):
            groups['open'].append(p)
        elif s.get('status') == 'tested':
            groups['pr'].append(p)
        elif s.get('status') == 'regression' and kr in ('proposed', 'approved'):
            groups['refresh'].append(p)
        elif s.get('status') == 'regression':
            groups['bug'].append(p)
            reasons[res.get('failure_reason') or 'other'].append(p)
            m = re.search(r'(?:Signing key on|Missing key) ([0-9A-F]{16,})', res.get('log_tail', ''))
            if m:
                keys[m.group(1)].append(p)
        elif s.get('status') == 'manual':
            groups['manual'].append(p)
        elif s.get('status') == 'superseded':
            groups['done'].append(p)
        elif p == 'teckit' or s.get('status') == 'guard-failed':
            groups['noverify'].append(p)
        else:
            groups['other'].append('%s (%s)' % (p, s.get('status')))
    n = len(eln)
    txt = ['Status of the ELN packages that verify sources with `%%gpgverify` or gpg, from '
           'the test runs in https://github.com/Jakuje/openpgpverify-migration (%s). %d packages '
           'are in scope; each was tested by running `%%prep` with the current and the '
           'converted spec in mock (rawhide, plus ELN where the spec has `%%{?rhel}` '
           'conditionals).' % (state.now()[:10], n), '']
    txt += ['**Ready for a PR** (%d): converted spec passes; patch and PR text under '
            '`proposals/`:' % len(groups['pr']), '', plist(groups['pr'], link=True), '']
    txt += ['**Ready after a keyring update** (%d): the keyring in dist-git is outdated; a '
            'newer copy of the same key from keyservers/WKD verifies. Waiting for my review '
            'of the refreshed keys:' % len(groups['refresh']), '',
            plist(groups['refresh'], link=True), '']
    txt += ['**Need upstream or maintainer action** (%d): no working key is published; these '
            'get bugs explaining the options:' % len(groups['bug']), '']
    for r, ps in sorted(reasons.items(), key=lambda kv: -len(kv[1])):
        txt.append('- %s: %s' % (REASON_TEXT.get(r, r), plist(ps)))
    shared = [(k, ps) for k, ps in keys.items() if len(ps) > 1]
    if shared:
        txt += ['', 'Some of them share one upstream key, so one key update fixes several:', '']
        for k, ps in sorted(shared, key=lambda kv: -len(kv[1])):
            txt.append('- `%s`: %s' % (k, plist(ps)))
    txt += ['', '**Call gpg/gpgv directly** (%d), hand-written PRs needed: %s' %
            (len(groups['manual']), plist(groups['manual'])), '',
            '**Already converted** in dist-git (%d): %s' % (len(groups['done']),
                                                            plist(groups['done'])), '',
            '**Open PR from someone else** (%d), skipped: %s' % (len(groups['open']),
                                                              plist(groups['open']))]
    if groups['noverify']:
        txt += ['', '**Verification disabled in the spec** (%d), nothing to convert: %s' %
                (len(groups['noverify']), plist(groups['noverify']))]
    if groups['other']:
        txt += ['', '**Other** (%d): %s' % (len(groups['other']), ', '.join(groups['other']))]
    missing = sorted(p for p in eln - issue
                     if st.get(p, {}).get('status') not in ('superseded', 'guard-failed'))
    # Checklist entries we don't cover: no source verification at all (only
    # BuildRequires: gnupg2, or gpg used as a tool), or already converted.
    extra = sorted(p for p in issue - eln if p not in st)
    txt += ['', '**Not in the checklist above** but in ELN and verifying with `%%gpgverify`: %s' %
            plist(missing), '',
            '**In the checklist but not verifying sources** (only `BuildRequires: gnupg2`, '
            'gpg used as a tool, or already done), so not covered by these PRs: %s' %
            plist(extra)]
    text = '\n'.join(txt) + '\n'
    if out:
        open(out, 'w').write(text)
    else:
        sys.stdout.write(text)


if __name__ == '__main__':
    main()
