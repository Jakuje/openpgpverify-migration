#!/usr/bin/python3 -I
"""Render the proposed dist-git change, PR text or bug text for packages.

Usage: render_proposals.py [--list FILE] [PKG...]

Writes proposals/PKG/ from the Phase 1 state and templates/:
  PR        status `tested`: 0001-*.patch (git format-patch of the commit a PR
            would carry, made in a scratch clone of work/PKG/dist-git at the
            tested commit) and PR.md
  draft PR  regression with a keyring refresh `proposed` (not yet approved):
            the same, with the refreshed keyring, marked as a draft
  bug       other regressions: BUG.md (Bugzilla fields + description)
and proposals/README.md, an index. Nothing is pushed or filed.
"""
import argparse
import datetime
import hashlib
import os
import re
import shutil
import string
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import phase1  # noqa: E402
import state  # noqa: E402

TEMPLATES = os.path.join(state.ROOT, 'templates')
OUT = os.path.join(state.ROOT, 'proposals')
AUTHOR = ('Jakub Jelen', 'jjelen@redhat.com')
CHANGELOG_LINE = 'Verify source signatures with openpgpverify (Sequoia)'
PATCH_NAME = '0001-Verify-source-signatures-with-openpgpverify.patch'

REASONS = {
    'sha1-cert': (
        'SHA-1 key self-signatures',
        "The signing key's own self-signatures (user ID certifications or subkey "
        "bindings) are made with SHA-1. The Fedora crypto policy rejects SHA-1, and "
        "Sequoia applies the policy to key bindings too; GnuPG doesn't check them. No "
        "newer copy of the key with modern self-signatures is published on "
        "keys.openpgp.org, keyserver.ubuntu.com or WKD.",
        "- Ask upstream to re-create the key's self-signatures with a modern hash and "
        "publish the updated key; renewing the expiry does that (`gpg --cert-digest-algo "
        "SHA512 --quick-set-expire FPR 2y`, and again with `'*'` for the subkeys). Then "
        "refresh the keyring in dist-git.\n"
        "- If upstream already signs with a newer key, switch the keyring to that key."),
    'sha1-sig': (
        'SHA-1 data signature',
        "The release signature itself is made with SHA-1 (or with a key algorithm such "
        "as DSA-1024 that the policy rejects). SHA-1 is not accepted for signatures "
        "over data because of collision attacks, and this won't be relaxed.",
        "- Ask upstream to sign releases with SHA-256 or better, ideally with a current "
        "key.\n"
        "- Until then the package can keep `%gpgverify`, or verify the tarball "
        "differently (for example against a checksum published over HTTPS)."),
    'v3-sig': (
        'OpenPGP v3 signature',
        "The release signature uses the version 3 signature format, which OpenPGP "
        "implementations have rejected since 2021.",
        "- Ask upstream to re-sign the release with a current key, if upstream is "
        "still active.\n"
        "- Otherwise, consider verifying against a checksum, or keep `%gpgverify` for "
        "now."),
    'expired': (
        'key expired before signing',
        "According to the keyring in dist-git, the signing key had already expired "
        "when the release was signed. Usually upstream extended the expiry later and "
        "the copy in dist-git is outdated. No newer copy is published on "
        "keys.openpgp.org, keyserver.ubuntu.com or WKD. GnuPG ignores expiry; Sequoia "
        "checks that the key was valid when the signature was made. (Signatures made "
        "while the key was valid keep verifying after it expires.)",
        "- Ask upstream to publish their current key (keys.openpgp.org, WKD or the "
        "project website), then update the keyring in dist-git."),
    'binding-after-signature': (
        'keyring lacks older self-signatures',
        "The keyring in dist-git only has self-signatures that are newer than the "
        "release signature, so for Sequoia the key wasn't bound yet when the release "
        "was signed. GnuPG doesn't check this. No copy with the older self-signatures "
        "is published.",
        "- Export the full key from upstream (with its older self-signatures) and "
        "update the keyring in dist-git."),
    'keybox': (
        'GnuPG keybox keyring',
        "The keyring file is in GnuPG's keybox format, which only GnuPG can read.",
        "- Convert it to an OpenPGP keyring: `gpg --no-default-keyring --keyring "
        "./FILE --export > FILE.gpg`, and use that file."),
    'concatenated-armor': (
        'several armored blocks in one file',
        "The signature file contains several ASCII-armored blocks concatenated. That "
        "is outside the OpenPGP format and Sequoia doesn't read it.",
        "- Keep only the signature by the key in the keyring, or dearmor and join "
        "the packets."),
}
GENERIC = ('verification fails',
           "`%openpgpverify` rejects a signature that `%gpgverify` accepts; see the "
           "output above.",
           "- Please have a look; I'm happy to help.")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def tmpl(name, **kw):
    return string.Template(open(os.path.join(TEMPLATES, name)).read()).substitute(**kw)


def short_args(args):
    return re.sub(r'/builddir/(new|old|pkg)/', '', args)


def sqv_excerpt(log_tail, n=12):
    """The sqv error lines between the verify call and the failure message."""
    lines = log_tail.splitlines()
    start = max((i for i, l in enumerate(lines) if 'openpgpverify --' in l), default=-1)
    out = []
    for l in lines[start + 1:]:
        if l.startswith('error: Bad exit status'):
            break
        out.append(l.rstrip())
    return '\n'.join(out[:n]) or log_tail[-1500:]


def add_changelog(text):
    """Entry for specs without %autochangelog, with the EVR of the latest entry
    (no Release bump, see README)."""
    m = re.search(r'(?m)^%changelog[ \t]*\n', text)
    if not m:
        return text, None
    head = re.search(r'(?m)^\*[^\n]*?(?:-\s*|\s)((?:\d+:)?[\w.+~^]+-[\w.+~^]+)\s*$',
                     text[m.end():])
    evr = head.group(1) if head else None
    date = datetime.date.today().strftime('%a %b %d %Y')
    entry = '* %s %s <%s>%s\n- %s\n\n' % (date, AUTHOR[0], AUTHOR[1],
                                         ' - ' + evr if evr else '', CHANGELOG_LINE)
    return text[:m.end()] + entry + text[m.end():], evr


def removed_brs(diff):
    return [l[1:].strip() for l in diff.splitlines()
            if l.startswith('-BuildRequires') and re.search(r'gpg|gnupg', l)]


def make_commit(pkg, s, refresh_files):
    """Commit the change in a scratch clone and return (patch text, notes)."""
    d = os.path.join(phase1.WORK, pkg)
    g, pr = os.path.join(d, 'dist-git'), os.path.join(d, 'pr')
    shutil.rmtree(pr, ignore_errors=True)
    if sh(['git', 'clone', '-q', '--no-hardlinks', g, pr]).returncode or \
            sh(['git', '-C', pr, 'checkout', '-q', '-b', 'openpgpverify',
                s['spec_commit']]).returncode:
        raise RuntimeError('cannot prepare a clone at %s' % s['spec_commit'])
    spec = open(os.path.join(d, pkg + '.opv.spec')).read()
    extra, evr = [], None
    if not s.get('autochangelog'):
        spec, evr = add_changelog(spec)
    open(os.path.join(pr, pkg + '.spec'), 'w').write(spec)
    for f in refresh_files:
        shutil.copy(os.path.join(d, 'refresh', f['file']), os.path.join(pr, f['file']))
        extra.append('Refresh %s from keyservers/WKD: same certificate(s), with '
                     'self-signatures our copy was missing.' % f['file'])
    body = tmpl('commit-message.txt',
                extra_body=('\n' + '\n'.join(extra) + '\n') if extra else '')
    sh(['git', '-C', pr, 'add', '-A'])
    env = dict(os.environ, GIT_AUTHOR_NAME=AUTHOR[0], GIT_AUTHOR_EMAIL=AUTHOR[1],
               GIT_COMMITTER_NAME=AUTHOR[0], GIT_COMMITTER_EMAIL=AUTHOR[1])
    if sh(['git', '-C', pr, 'commit', '-q', '-F', '-'], input=body, env=env).returncode:
        raise RuntimeError('commit failed')
    patch = sh(['git', '-C', pr, 'format-patch', '-1', '--stdout', '--binary']).stdout
    diff = sh(['git', '-C', pr, 'show', '--format=', pkg + '.spec']).stdout
    return patch, diff, evr


def render_pr(pkg, s, draft):
    kr = s.get('keyring_refresh') or {}
    files = [f for f in kr.get('files', []) if f.get('changed')] if draft or \
        s.get('keyring_refresh_applied') else []
    patch, diff, evr = make_commit(pkg, s, files)
    res = s['results'][0]
    n_old = len(res.get('old_calls', []))
    changes = ['- `%%gpgverify` → `%%openpgpverify` (%d call%s; the macro keeps the same form '
               'and options)' % (n_old, '' if n_old == 1 else 's')]
    if re.search(r'(?m)^\+BuildRequires\s*:\s*openpgpverify', diff):
        changes.append('- added `BuildRequires: openpgpverify`; nothing pulls it into the '
                       'buildroot implicitly (gpgverify comes in via redhat-rpm-config)')
    for br in removed_brs(diff):
        if s.get('rhel_conditional'):
            continue
        changes.append('- dropped `%s`, only needed for `%%gpgverify`' % br)
    if s.get('rhel_conditional'):
        changes.append('- the spec has RHEL conditionals, so it is likely shared with EPEL, '
                       'where openpgpverify is not available: `%if 0%{?fedora} || '
                       '0%{?rhel} >= 11` uses openpgpverify, otherwise everything stays '
                       'as it was')
    for f in files:
        changes.append('- refreshed keyring `%s` (see below)' % f['file'])
    if evr is not None or not s.get('autochangelog'):
        changes.append('- changelog entry%s, without a Release bump' %
                       (' (%s)' % evr if evr else ''))
    chroots = []
    for r in s['results']:
        c = r['chroot']
        if r.get('outcome') == 'not-buildable':
            c += ', where even the current spec cannot install its build dependencies'
        chroots.append(c)
    calls_new = len(res.get('new_calls', []))
    if draft:
        result_old, result_new = 'pass', ('fails with the keyring in dist-git; **passes '
                                          'with the refreshed keyring** (sqv run directly)')
    else:
        result_old = 'pass' if all(c['rc'] == 0 for c in res.get('old_calls', [])) else 'FAIL'
        result_new = 'pass' if all(c['rc'] == 0 for c in res.get('new_calls', [])) else 'FAIL'
    refresh = ''
    if files:
        review = open(os.path.join(state.ROOT, kr['review'])).read()
        diffs = re.findall(r'```diff\n(.*?)```', review, re.S)
        reason = (REASONS.get(res.get('failure_reason')) or GENERIC)[0]
        refresh = ('\n### Keyring refresh\n\n'
                   '`%%openpgpverify` rejected the signature with the keyring in dist-git '
                   '(%s), while `%%gpgverify` ignores that. The same certificate, looked up '
                   'by fingerprint (%s), has self-signatures our copy is missing (a renewed '
                   'expiry, modern hashes or the older binding history), so this PR updates '
                   'the keyring. No key was added or removed. Please check the fingerprint '
                   'against upstream:\n\n%s\n\nWhat changed in the certificate (`sq '
                   'inspect`):\n\n```diff\n%s```\n'
                   % (reason, '; '.join(sorted({v for f in files for v in f['found_via']})),
                      '\n'.join('- `%s`' % fp for f in files for fp in f['fingerprints']),
                      ''.join(diffs)))
    notes = ['- Rawhide only. Whether to merge it into other branches is up to you; '
             'openpgpverify is in Fedora 43 and later' +
             ('.' if s.get('rhel_conditional') else
              ', but not in EPEL yet, so please keep `%gpgverify` on EPEL branches.')]
    if s.get('gnupg2_action') in ('review', 'keep') and not s.get('rhel_conditional'):
        notes.append('- `BuildRequires: gnupg2` is kept: the spec has a `%check` section '
                     'or uses gpg elsewhere, and tests may need it. If it was only there '
                     'for the signature check, it can go too.')
    notes.append('- No Release bump: nothing changes in the built packages, so no rebuild '
                 'is needed now. The new check runs with your next build.')
    if s.get('stage') and s['stage'] != '-bp':
        notes.append('- The verification runs outside `%prep`. Moving it to the start of '
                     '`%prep` would check the sources before anything else uses them.')
    text = tmpl('pr-description.md',
                changes='\n'.join(changes) + '\n', stage='rpmbuild %s' % s.get('stage', '-bp'),
                chroots=', '.join(chroots), calls_old=n_old, calls_new=calls_new,
                result_old=result_old, result_new=result_new,
                tested_on=s['updated'][:10], commit=s['spec_commit'][:12],
                sqv_version=s.get('sqv_version') or '?',
                refresh_section=refresh,
                notes_section='\n### Notes\n\n' + '\n'.join(notes) + '\n')
    title = 'Verify source signatures with openpgpverify'
    if draft:
        text = ('> **DRAFT, not to be opened yet:** the keyring refresh below still needs '
                'a human review (`scripts/refresh_keys.py show %s`).\n\n' % pkg) + text
    return patch, '# %s\n\n%s' % (title, text)


def render_bug(pkg, s):
    res = s['results'][0]
    bad = [c for c in res.get('new_calls', []) if c['rc'] != 0][0]
    short, why, actions = REASONS.get(res.get('failure_reason')) or GENERIC
    kr = s.get('keyring_refresh') or {}
    if kr.get('status') in ('no-update', 'not-found') and res.get('failure_reason') not in (
            'sha1-cert', 'expired', 'binding-after-signature'):
        why += ' (A refreshed key from keyservers/WKD doesn\'t help either.)'
    return tmpl('bug.md', package=pkg, reason_short=short, commit=s['spec_commit'][:12],
                call='%%openpgpverify %s' % short_args(bad['args']),
                log_excerpt=sqv_excerpt(res.get('log_tail', '')), reason_text=why,
                actions=actions)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', default=os.path.join(state.ROOT, 'data', 'pilot.txt'))
    ap.add_argument('packages', nargs='*')
    a = ap.parse_args()
    pkgs = a.packages or list(dict.fromkeys(l.strip() for l in open(a.list) if l.strip()))
    st = state.load()
    index = []
    for pkg in pkgs:
        s = st.get(pkg)
        d = os.path.join(OUT, pkg)
        shutil.rmtree(d, ignore_errors=True)
        status = (s or {}).get('status')
        if status in ('manual', 'superseded', 'skipped', 'error', 'guard-failed', 'both-fail'):
            index.append((pkg, 'skipped', '%s: %s' % (status, s.get('outcome_detail') or '')))
            continue
        if not s or not s.get('results'):
            index.append((pkg, 'skipped', 'not tested'))
            continue
        spec = os.path.join(phase1.WORK, pkg, 'dist-git', pkg + '.spec')
        kr = (s.get('keyring_refresh') or {}).get('status')
        if hashlib.sha256(open(spec, 'rb').read()).hexdigest() != s.get('spec_sha256'):
            index.append((pkg, 'skipped', 'dist-git changed since Phase 1; re-run it'))
            continue
        os.makedirs(d)
        if status == 'tested' or (status == 'regression' and kr in ('proposed', 'approved')):
            draft = status != 'tested'
            patch, text = render_pr(pkg, s, draft)
            open(os.path.join(d, PATCH_NAME), 'w').write(patch)
            open(os.path.join(d, 'PR.md'), 'w').write(text)
            what = 'draft PR' if draft else 'PR'
            why = 'keyring refresh %s' % kr if draft else (
                'with approved keyring refresh' if s.get('keyring_refresh_applied') else '')
            index.append((pkg, what, why))
        else:
            open(os.path.join(d, 'BUG.md'), 'w').write(render_bug(pkg, s))
            index.append((pkg, 'bug', s['results'][0].get('failure_reason') or ''))
        print('%-24s %s' % (pkg, index[-1][1]), flush=True)
    lines = ['# Proposals', '',
             'Generated %s by `scripts/render_proposals.py` from the Phase 1 state. Nothing '
             'here has been opened or filed.' % state.now(), '',
             '- **PR**: `0001-*.patch` is the commit a PR would carry (`git am` applies it '
             'to dist-git at the tested commit); `PR.md` is the PR title and description.',
             '- **draft PR**: the same, but it includes a keyring refresh that hasn\'t been '
             'reviewed yet.',
             '- **bug**: `BUG.md`, the Bugzilla fields and description for packages that '
             'need upstream or maintainer action first.', '',
             '| Package | Proposal | Notes |', '|---|---|---|']
    for pkg, what, why in index:
        link = '[%s](%s/)' % (pkg, pkg) if what != 'skipped' else pkg
        lines.append('| %s | %s | %s |' % (link, what, why.replace('|', '\\|')))
    open(os.path.join(OUT, 'README.md'), 'w').write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
