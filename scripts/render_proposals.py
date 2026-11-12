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
import hashlib
import os
import re
import shutil
import string
import subprocess
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import convert  # noqa: E402
import phase1  # noqa: E402
import state  # noqa: E402

TEMPLATES = os.path.join(state.ROOT, 'templates')
OUT = os.path.join(state.ROOT, 'proposals')
AUTHOR = ('Jakub Jelen', 'jjelen@redhat.com')
LOOKASIDE_TO_GIT_MAX = 1024 * 1024   # bytes; bigger keyrings stay in the lookaside cache
PATCH_NAME = '0001-Verify-source-signatures-with-openpgpverify.patch'

# How to re-create SHA-1 self-signatures so that old signatures stay valid (Clemens Lang).
RESIGN_ARTICLE = ('[Updating GPG keys for Fedora and RHEL]'
                  '(https://www.redhat.com/en/blog/updating-gpg-keys-for-fedora-and-rhel)')
# Re-signing first; backdated self-signatures only when re-signing is not an option.
REFRESH_SHA256 = (
    "- Ask upstream to refresh the key's self-signatures with SHA-256 and publish the "
    "updated key (keys.openpgp.org, WKD or the project website):\n\n"
    "      gpg --cert-digest-algo SHA256 --quick-set-expire FPR 2030-12-31\n"
    "      gpg --cert-digest-algo SHA256 --quick-set-expire FPR 2030-12-31 '*'\n\n"
    "  Use an absolute expiry date (or `0`). Releases signed after this verify.\n")
RESIGN_RELEASE = (
    "- For the release already in Fedora, ask upstream to sign the same tarball again with "
    "the updated key and publish the new signature (the tarball doesn't change), or wait "
    "for the next release. Then update the keyring and the signature in dist-git.\n")
BACKDATE_LAST = (
    "- Only if re-signing is not an option, upstream (only the key owner can do this) "
    "can date the new self-signatures one second after the key (or its newest subkey) "
    "was created, so that the existing release signatures verify too. Backdating is "
    "unusual and easy to get wrong, so it is a last resort; %s describes how "
    "(`gpg --faked-system-time \"$((CT + 1))!\" --cert-digest-algo SHA256 "
    "--quick-set-expire ...`, with `CT` that creation time).\n"
    "- If upstream doesn't respond, the package can keep `%%gpgverify` for now; nothing "
    "breaks until it is removed." % RESIGN_ARTICLE)


REASONS = {
    'sha1-cert': (
        'SHA-1 key self-signatures',
        "The signing key's own self-signatures (user ID certifications or subkey "
        "bindings) are made with SHA-1. The Fedora crypto policy rejects SHA-1, and "
        "Sequoia applies the policy to key bindings too; GnuPG doesn't check them. No "
        "newer copy of the key with modern self-signatures is published on "
        "keys.openpgp.org, keyserver.ubuntu.com or WKD.",
        REFRESH_SHA256 + RESIGN_RELEASE +
        "- If upstream already signs with a newer key, switch the keyring to that key.\n" +
        BACKDATE_LAST),
    'sha1-sig': (
        'SHA-1 data signature',
        "The release signature itself is made with SHA-1. SHA-1 is not accepted for "
        "signatures over data because of collision attacks, and this won't be relaxed.",
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
        "project website), then update the keyring in dist-git. If the expiry was "
        "extended before the release was signed, that is all.\n" +
        RESIGN_RELEASE.replace('with the updated key', 'with the extended key') +
        BACKDATE_LAST),
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
REASONS.update({
    'unparseable-cert': (
        'keyring contains a key sqv cannot read',
        "The keyring contains a certificate that Sequoia can't parse (typically an "
        "old version 3 key, common in long-lived KEYS files). GnuPG skips such keys "
        "silently; sqv rejects the whole keyring, even though the key that signed the "
        "release is fine.",
        "- Trim the keyring to the keys that sign releases (for example `gpg --import "
        "KEYS` into a temporary keyring, then `gpg --export FPR... > keyring.gpg`), and "
        "use that file in the spec."),
    'weak-key': (
        'signing key algorithm rejected',
        "The release is signed with a key whose algorithm the crypto policy rejects "
        "(DSA, or RSA shorter than 2048 bits); for a signing subkey, its primary key "
        "counts too. Neither a new release signature nor new self-signatures with this "
        "key will help. (DSA-1024 can only use 160-bit hashes, which is also why such "
        "signatures are SHA-1.)",
        "- Ask upstream to create a new key (for example Ed25519 or RSA 3072+), publish "
        "it, and sign releases with it using SHA-256 or better. Then switch the keyring "
        "to it.\n"
        "- Until then the package can keep `%gpgverify`, or verify the tarball "
        "differently (for example against a checksum published over HTTPS)."),
})
REASONS['v3-key-sha1-cert'] = (
    'unreadable v3 key in keyring, SHA-1 self-signatures',
    "Two things stand in the way. The keyring contains a version 3 certificate, which "
    "Sequoia can't parse; GnuPG skips it silently, but sqv rejects the whole keyring. "
    "With the keyring trimmed to the signing key (`gpg --import` into a temporary "
    "keyring, then `gpg --export FPR`), sqv reads it, but the signing key's own "
    "self-signatures are made with SHA-1, which the Fedora crypto policy rejects. No "
    "newer copy of the key with modern self-signatures is published on "
    "keys.openpgp.org, keyserver.ubuntu.com or WKD.",
    REFRESH_SHA256 +
    "- Use a keyring with only the keys that sign releases (`gpg --import KEYS` into a "
    "temporary keyring, then `gpg --export FPR... > keyring.gpg`), so it has no v3 key.\n" +
    RESIGN_RELEASE + BACKDATE_LAST)
# sha1-sig wins in phase1, but sqv often reports the key binding first: say both.
REASONS['sha1-sig-and-cert'] = (
    'SHA-1 data signature and key self-signatures',
    "Two things use SHA-1, which the Fedora crypto policy rejects. The release "
    "signature itself is made with SHA-1; SHA-1 is not accepted for signatures over "
    "data because of collision attacks, and this won't be relaxed. The signing key's "
    "own self-signatures (user ID certifications or subkey bindings) are SHA-1 too, "
    "and that is what sqv reports first above; GnuPG doesn't check them.",
    REFRESH_SHA256.replace('Releases signed after this verify.',
                           'A new SHA-256 release signature alone still fails while the '
                           'key is only bound with SHA-1.') +
    "- Then ask upstream to sign releases with SHA-256 (`gpg --digest-algo SHA256`, or "
    "`personal-digest-preferences SHA256` in `gpg.conf`): the current release again, or "
    "the next one. Then update the keyring and the signature in dist-git.\n"
    "- If upstream already signs with a newer key, ask them to use SHA-256 with it and "
    "switch the keyring to that key.\n"
    "- Until then the package can keep `%gpgverify`, or verify the tarball "
    "differently (for example against a checksum published over HTTPS).")
GENERIC = ('verification fails',
           "`%openpgpverify` rejects a signature that `%gpgverify` accepts; see the "
           "output above.",
           "- Please have a look; I'm happy to help.")


CONVERT_METHODS = ('keyserver-signers', 'gpg-export')


def convert_why(f):
    """Why sqv cannot use a keyring that propose-convert rebuilt."""
    if f.get('skipped_v3'):
        return ('it holds %d v3 (PGP 2) key%s, which Sequoia does not parse, so sqv rejects '
                'the whole file (GnuPG skips such keys silently)'
                % (f['skipped_v3'], '' if f['skipped_v3'] == 1 else 's'))
    return 'its copy of the signing key is outdated'


def dropped_text(f, md=False):
    """The certificates a rebuilt keyring dropped: listed, or counted when many."""
    d = f['dropped']
    if len(d) > 5:
        return '%d certificates of other people' % len(d)
    return ', '.join(('`%s`' if md else '%s') % x for x in d)


def convert_text(f):
    """One sentence for the commit message about a rebuilt keyring."""
    new = os.path.basename(f.get('new_file') or f['file'])
    if f['method'] == 'gpg-export':
        s = ('Convert upstream\'s KEYS file (%s) with GnuPG into %s, a plain OpenPGP '
             'keyring with every key GnuPG reads from it (%d); sqv cannot read the KEYS '
             'file itself: %s.' % (f['url'], new, len(f['fingerprints']), convert_why(f)))
    else:
        s = ('Replace %s the keyserver copy of the key that signs releases (%s), '
             'because sqv cannot use the old keyring: %s.%s' % (
                 'the content of %s with' % f['file'] if new == f['file'] else
                 '%s with %s,' % (f['file'], new),
                 ', '.join(f['fingerprints']), convert_why(f),
                 ' The other certificates in it are dropped (%s).' % dropped_text(f)
                 if f.get('dropped') else ''))
    if f.get('new_file'):
        s += (' Its Source line names the new file instead of %s, which is not what the '
              'file holds any more.' % (f.get('old_source') or f['file']))
    return s


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


def removed_brs(diff):
    return [l[1:].strip() for l in diff.splitlines()
            if l.startswith('-BuildRequires') and re.search(r'gpg|gnupg', l)]


def split_series(mbox):
    """Split `git format-patch --stdout` output into (file name, patch) pairs
    named like `git format-patch` names them."""
    parts = re.split(r'(?m)^(?=From [0-9a-f]{40} Mon Sep 17 00:00:00 2001$)', mbox)
    parts = [x for x in parts if x.strip()]
    out = []
    for i, x in enumerate(parts, 1):
        subj = re.search(r'(?m)^Subject: \[PATCH(?: \d+/\d+)?\] (.*)$', x).group(1)
        out.append(('%04d-%s.patch' % (i, re.sub(r'[^A-Za-z0-9]+', '-', subj).strip('-')), x))
    return out


def spec_comment(text, pkg, files):
    """The spec comments that go with keyring updates (see refresh_keys.py)."""
    for f in files:
        if f.get('source_url'):
            text = convert.source_to_url(text, pkg, os.path.basename(f['file']),
                                         f['source_url'])[0]
        elif f.get('spec_commands'):
            name = os.path.basename(f['file'])
            if f.get('new_file'):
                text = convert.source_to_file(text, pkg, name,
                                              os.path.basename(f['new_file']))[0]
                name = os.path.basename(f['new_file'])
            text = convert.refresh_comment(
                text, pkg, name, f['spec_commands'],
                *([f['spec_header']] if f.get('spec_header') else []))[0]
    return text


def make_commit(pkg, s, refresh_files):
    """Commit the change in a scratch clone and return (patch series, spec diff).
    A keyring update is a commit of its own, before the openpgpverify one
    (maintainers asked for that: it is a different change)."""
    d = os.path.join(phase1.WORK, pkg)
    g, pr = os.path.join(d, 'dist-git'), os.path.join(d, 'pr')
    shutil.rmtree(pr, ignore_errors=True)
    if sh(['git', 'clone', '-q', '--no-hardlinks', g, pr]).returncode or \
            sh(['git', '-C', pr, 'checkout', '-q', '-b', 'openpgpverify',
                s['spec_commit']]).returncode:
        raise RuntimeError('cannot prepare a clone at %s' % s['spec_commit'])
    env = dict(os.environ, GIT_AUTHOR_NAME=AUTHOR[0], GIT_AUTHOR_EMAIL=AUTHOR[1],
               GIT_COMMITTER_NAME=AUTHOR[0], GIT_COMMITTER_EMAIL=AUTHOR[1])
    spec = os.path.join(pr, pkg + '.spec')

    def commit(body):
        sh(['git', '-C', pr, 'add', '-A'])
        p = sh(['git', '-C', pr, 'commit', '-q', '-F', '-'], input=body, env=env)
        if p.returncode:
            raise RuntimeError('%s: commit failed: %s' % (pkg, (p.stdout + p.stderr).strip()))

    def wrap(lines):
        return [textwrap.fill(e, 72, break_long_words=False, break_on_hyphens=False)
                for e in lines]
    if refresh_files:
        key, moved = [], []
        for f in refresh_files:
            if f.get('new_file'):
                # The keyring is named like its Source URL: drop the old file
                # (from git, or from the lookaside "sources") and add the new one.
                if sh(['git', '-C', pr, 'ls-files', '--error-unmatch', f['file']]).returncode:
                    for meta in ('sources', '.gitignore'):
                        path = os.path.join(pr, meta)
                        if os.path.exists(path):
                            keep = [l for l in open(path).read().splitlines() if not re.search(
                                r'(^|[ (/])%s(\)|$)' % re.escape(f['file']), l)]
                            open(path, 'w').write(''.join(l + '\n' for l in keep))
                else:
                    sh(['git', '-C', pr, 'rm', '-q', f['file']])
                shutil.copy(os.path.join(d, 'refresh', f['file']), os.path.join(pr, f['new_file']))
                sh(['git', '-C', pr, 'add', '-f', f['new_file']])
                if f.get('method') in CONVERT_METHODS:
                    key += [convert_text(f), 'The commands are in the comment above its '
                            'Source line.']
                    continue
                key.append('Replace %s with %s, the key upstream publishes at %s (byte for '
                           'byte); its Source line is now that URL.%s' % (
                               f['file'], os.path.basename(f['new_file']), f['url'],
                               ' The file holds only %s; the other certificate(s) in the old '
                               'keyring (%s) are dropped.' % (', '.join(f['fingerprints']),
                                                               ', '.join(f['dropped']))
                               if f.get('dropped') else ''))
                continue
            shutil.copy(os.path.join(d, 'refresh', f['file']), os.path.join(pr, f['file']))
            if sh(['git', '-C', pr, 'ls-files', '--error-unmatch', f['file']]).returncode:
                # In the lookaside cache, which a PR cannot upload to.
                if os.path.getsize(os.path.join(pr, f['file'])) > LOOKASIDE_TO_GIT_MAX:
                    raise RuntimeError('%s: %s is in the lookaside cache and too big to move '
                                       'into git; the maintainer has to upload it'
                                       % (pkg, f['file']))
                for meta in ('sources', '.gitignore'):
                    path = os.path.join(pr, meta)
                    if os.path.exists(path):
                        keep = [l for l in open(path).read().splitlines()
                                if not re.search(r'(^|[ (/])%s(\)|$)' % re.escape(f['file']), l)]
                        open(path, 'w').write(''.join(l + '\n' for l in keep))
                sh(['git', '-C', pr, 'add', '-f', f['file']])
                moved.append(f['file'])
            if f.get('kind') == 'signature':
                key.append('Replace %s with the release signature upstream made again with '
                           'the updated key (%s), from %s.' % (
                               f['file'], ', '.join('%s, %s' % (x['hash'], x['created'][:10])
                                                    for x in f['signatures']), f['url']))
            elif f.get('method') in CONVERT_METHODS:
                key.append(convert_text(f))
            elif f.get('method', '').startswith('key-url'):
                key.append('Rebuild %s from the key upstream publishes at %s%s%s (same '
                           'certificate(s)).' % (
                               f['file'], f['url'],
                               ', merged into the existing keyring' if f.get('url_fingerprints')
                               and sorted(f['url_fingerprints']) != sorted(f['fingerprints'])
                               else '',
                               ', completed from keyservers/WKD with the older '
                               'self-signatures and subkey bindings the release needs'
                               if f['method'].endswith('keyserver') else ''))
            elif f.get('method') == 'upstream-url' and f.get('dropped'):
                key.append('Replace %s with the current key at %s. That file holds only %s; '
                           'the other certificate(s) in the keyring (%s) are dropped.' % (
                               f['file'], f['url'], ', '.join(f['fingerprints']),
                               ', '.join(f['dropped'])))
            elif f.get('method') == 'upstream-url':
                key.append('Update %s to the current copy at %s%s (same certificate(s)).' % (
                    f['file'], f['url'], '' if f.get('spec_commands') else
                    ', the URL the spec names for it'))
            else:
                key.append('Refresh %s from keyservers: same certificate(s), with '
                           'self-signatures our copy was missing.%s' % (
                               f['file'], ' The GnuPG keybox becomes a plain OpenPGP '
                               'keyring, which sqv can read.' if f.get('keybox') else ''))
            if f.get('spec_commands'):
                key.append('The commands are in the comment above its Source line.')
        key += ['%s was in the lookaside cache, which a pull request cannot update, so it '
                'moves into git (dropped from sources).' % m for m in moved]
        # The current spec with only the keyring comment changed.
        text = spec_comment(open(spec).read(), pkg, refresh_files)
        open(spec, 'w').write(text)
        n = len([f for f in refresh_files if f.get('kind') != 'signature'])
        resigned = any(f.get('kind') == 'signature' for f in refresh_files)
        commit('Update the upstream signing key%s%s\n\n%s\n\nThe current key is needed to '
               'verify the release signature with\nopenpgpverify (sqv), which checks that '
               'the key was valid when the\nrelease was signed.\n\nAssisted-by: Claude '
               'Opus 5.5\n' % ('' if n == 1 else 's',
                                ' and the release signature' if resigned else '',
                                '\n'.join(wrap(key))))
    # Exactly the spec Phase 1 tested (incl. the Release bump done in the chroot).
    shutil.copy(os.path.join(d, pkg + '.opv.spec'), spec)
    if refresh_files and not s.get('keyring_refresh_applied'):
        # Draft: phase1.py adds this comment once the refresh is approved.
        text = spec_comment(open(spec).read(), pkg, refresh_files)
        open(spec, 'w').write(text)
    extra = []
    if s.get('raw_rewritten'):
        lead = ('Replace the direct GnuPG verification with %openpgpverify, which\n'
                'uses Sequoia sqv, as part of the Fedora 45 Change\n'
                'https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify')
    else:
        lead = ('Replace the GnuPG-based %gpgverify with %openpgpverify, which uses\n'
                'Sequoia sqv and takes the same options, as part of the Fedora 45 Change\n'
                'https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify')
    if s.get('release_bumped'):
        extra.append('Release bumped with a changelog entry.')
    body = tmpl('commit-message.txt', lead=lead,
                extra_body=('\n' + '\n'.join(wrap(extra)) + '\n') if extra else '')
    commit(body)
    n = 2 if refresh_files else 1
    # bytes, not text: universal newlines would turn a keyring's CRLF into LF
    # and the patch would no longer apply
    patch = subprocess.run(['git', '-C', pr, 'format-patch', '-%d' % n, '--stdout', '--binary'],
                           capture_output=True).stdout.decode('utf-8', 'surrogateescape')
    diff = sh(['git', '-C', pr, 'diff', s['spec_commit'], 'HEAD', '--', pkg + '.spec']).stdout
    return patch, diff


def render_pr(pkg, s, draft):
    kr = s.get('keyring_refresh') or {}
    files = [f for f in kr.get('files', []) if f.get('changed')] if draft or \
        s.get('keyring_refresh_applied') else []
    if not s.get('autochangelog') and not s.get('autorelease') and not s.get('release_bumped'):
        raise RuntimeError('spec needs a Release bump; re-run phase1.py')
    patch, diff = make_commit(pkg, s, files)
    sigs = [f for f in files if f.get('kind') == 'signature']
    files = [f for f in files if f.get('kind') != 'signature']
    res = s['results'][0]
    n_old = len(res.get('old_calls', []))
    raw = s.get('raw_rewritten')
    if raw:
        tools = sorted({c['tool'] for c in res.get('old_calls', [])} - {'gpgverify'})
        old_tool = ', '.join('`%s`' % x for x in tools) or '`gpgv`'
        desc = os.path.join(convert.MANUAL, pkg + '.md')
        changes = [open(desc).read().strip() if raw == 'manual' and os.path.exists(desc) else
                   '- the direct %s call is replaced by `%%{openpgpverify}` with the same '
                   'keyring, signature and data' % old_tool]
        if re.search(r'(?m)^[-+].*%\{?gpgverify', diff):
            changes.append('- `%gpgverify` → `%openpgpverify` for the existing macro call')
    else:
        old_tool = '`%gpgverify`'
        changes = ['- `%%gpgverify` → `%%openpgpverify` (%d call%s; the macro keeps the same '
                   'form and options)' % (n_old, '' if n_old == 1 else 's')]
    if re.search(r'(?m)^\+BuildRequires\s*:\s*openpgpverify', diff):
        changes.append('- added `BuildRequires: openpgpverify`; nothing pulls it into the '
                       'buildroot implicitly (gpgverify comes in via redhat-rpm-config)')
    for br in removed_brs(diff):
        changes.append('- dropped `%s`, only needed for %s' %
                       (br, 'the GnuPG verification' if raw else '`%gpgverify`'))
    for f in files:
        if f.get('method') in CONVERT_METHODS:
            new = os.path.basename(f.get('new_file') or f['file'])
            changes.append('- %s keyring `%s`%s (see below); the comment above its `Source` '
                           'line shows the commands' % (
                               'converted upstream\'s KEYS file into the' if
                               f['method'] == 'gpg-export' else 'replaced the keyring with the '
                               'signing key from keyservers,', new,
                               ', which the `Source` line now names' if f.get('new_file') else ''))
            if re.search(r'(?m)^-SHA512 \(%s\) = ' % re.escape(f['file']), patch):
                changes.append('- `%s` is no longer used; its line in `sources` is dropped'
                               % f['file'])
            continue
        if re.search(r'(?m)^-SHA512 \(%s\) = |^-[0-9a-f]{32,}  %s$'
                     % (re.escape(f['file']), re.escape(f['file'])), patch):
            changes.append('- `%s` was in the lookaside cache, which a PR cannot update, so '
                           'it moves into git (its line in `sources` is dropped)' % f['file'])
        commented = re.search(r'(?m)^\+#   mv %s\.new ' % re.escape(os.path.basename(f['file'])),
                              diff)
        if f.get('method', '').startswith('key-url'):
            changes.append('- rebuilt keyring `%s` from the upstream key at %s%s (see below); '
                           'the comment above its `Source` line shows the commands'
                           % (f['file'], f['url'], ', completed from keyservers/WKD'
                              if f['method'].endswith('keyserver') else ''))
            continue
        if f.get('new_file'):
            changes.append('- replaced keyring `%s` with `%s` from %s; its `Source` line is now '
                           'that URL%s (see below)' % (
                               f['file'], os.path.basename(f['new_file']), f['url'],
                               '; **%d other certificate(s) are dropped**' % len(f['dropped'])
                               if f.get('dropped') else ''))
            continue
        if f.get('method') == 'upstream-url' and f.get('dropped'):
            changes.append('- replaced keyring `%s` with the upstream key from %s; **%d other '
                           'certificate(s) are dropped** (see below)'
                           % (f['file'], f['url'], len(f['dropped'])))
            continue
        if f.get('method') == 'upstream-url':
            changes.append('- updated `%s` to the current upstream copy from the URL in the '
                           'spec (see below)' % f['file'])
            continue
        changes.append('- refreshed keyring `%s` (see below)%s' % (
            f['file'], '; the comment above its `Source` line now shows the commands for '
            'refreshing it' if commented else ''))
    for f in sigs:
        changes.append('- replaced the release signature `%s` with the one upstream made again '
                       'with the updated key (see below)%s' % (
                           f['file'], '; it was in the lookaside cache, which a PR cannot '
                           'update, so it moves into git (its line in `sources` is dropped)'
                           if re.search(r'(?m)^-SHA512 \(%s\) = |^-[0-9a-f]{32,}  %s$' % (
                               re.escape(f['file']), re.escape(f['file'])), patch) else ''))
    rel = re.findall(r'(?m)^([-+])Release:\s*(.*)$', diff)
    if rel:
        changes.append('- Release bumped (`%s` → `%s`) with a changelog entry' %
                       (dict(rel).get('-', '?').strip(), dict(rel).get('+', '?').strip()))
    chroots = []
    for r in s['results']:
        c = r['chroot']
        if r.get('outcome') == 'not-buildable':
            c += ', where even the current spec cannot install its build dependencies'
        elif r.get('outcome') == 'not-verified':
            c += ', where the spec does not verify the sources (conditional)'
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
        # A retest with the refresh passes; the bug diagnosis keeps the reason.
        reason = (REASONS.get(res.get('failure_reason') or s.get('bug_reason')) or GENERIC)[0]
        keybox = any(f.get('keybox') for f in files)
    if files and kr.get('method') in CONVERT_METHODS:
        f = files[0]
        new = os.path.basename(f.get('new_file') or f['file'])
        if f['method'] == 'gpg-export':
            refresh = ('\n### Keyring update\n\n`%%openpgpverify` cannot use upstream\'s '
                       'KEYS file: %s. This PR converts it with GnuPG into `%s`, a plain '
                       'OpenPGP keyring. It keeps every key GnuPG reads from the KEYS file '
                       '(%d certificates), so releases by any of the release managers listed '
                       'there keep verifying. Exactly these commands (also in the comment '
                       'above the keyring\'s `Source` line, for the next update):\n\n```\n%s'
                       '\n```\n\nThe current release is signed by:\n\n%s\n%s'
                       % (convert_why(f), new, len(f['fingerprints']),
                          '\n'.join(f['commands']),
                          '\n'.join('- `%s`' % fp for fp in f.get('signers', [])),
                          ''.join('\nCompared with the KEYS file in the lookaside cache, %s.\n'
                                  % '; '.join(x for x in (
                                      'upstream has added %s' % ', '.join(
                                          '`%s`' % a for a in f['added']) if f.get('added')
                                      else '',
                                      'upstream has removed %s' % ', '.join(
                                          '`%s`' % a for a in f['dropped'])
                                      if f.get('dropped') else '') if x)
                                  for _ in [0] if f.get('added') or f.get('dropped'))))
        else:
            refresh = ('\n### Keyring update\n\n`%%openpgpverify` cannot use the keyring in '
                       'dist-git: %s. This PR replaces it with the keyserver copy of the key '
                       'that signed the release, looked up by fingerprint (%s), with exactly '
                       'this command (also in the comment above the keyring\'s `Source` line, '
                       'for the next update):\n\n```\n%s\n```\n\nPlease check the '
                       'fingerprint against upstream:\n\n%s\n\n%sWhat changed in the signing '
                       'certificate (`sq inspect`):\n\n```diff\n%s```\n'
                       % (convert_why(f), '; '.join(f.get('found_via') or ['-']),
                          '\n'.join(f['commands']),
                          '\n'.join('- `%s`' % fp for fp in f['fingerprints']),
                          ('Dropped from the keyring (not used for the current release; add '
                           'them back if releases may be signed with them):\n\n%s\n\n'
                           % ('\n'.join('- `%s`' % d for d in f['dropped'])
                              if len(f['dropped']) <= 5 else '- the other %d certificates '
                              'of `%s`' % (len(f['dropped']), f['file'])))
                          if f.get('dropped') else '', ''.join(diffs)))
    elif files and kr.get('method', '').startswith('key-url'):
        ks = kr['method'].endswith('keyserver')
        refresh = ('\n### Keyring update\n\n`%%openpgpverify` rejected the signature with '
                   'the keyring in dist-git (%s), while %s ignores that. %s'
                   'The keyring is rebuilt from that key%s, with exactly these commands '
                   '(also in the comment above the keyring\'s `Source` line, for the next '
                   'update):\n\n```\n%s\n```\n\nFingerprints (unchanged):\n\n%s\n\n'
                   'What changed in the certificate (`sq inspect`):\n\n```diff\n%s```\n'
                   % (reason, old_tool,
                      'Upstream publishes the current key at %s. ' % ', '.join(
                          sorted({f['url'] for f in files})) +
                      ('That copy has only the latest self-signatures, so it is completed from '
                       'keyservers/WKD (looked up by fingerprint, %s), which have the older '
                       'self-signatures and subkey bindings that were valid when the release '
                       'was signed. ' % '; '.join(sorted({v for f in files
                                                          for v in f.get('found_via', [])}))
                       if ks else ''),
                      ''.join(', merged into the existing keyring (the other keys stay)'
                              for f in files[:1] if f.get('url_fingerprints') and
                              sorted(f['url_fingerprints']) != sorted(f['fingerprints'])),
                      '\n'.join(c for f in files for c in f['commands']),
                      '\n'.join('- `%s`' % fp for f in files for fp in f['fingerprints']),
                      ''.join(diffs)))
    elif files and kr.get('method') == 'upstream-url':
        dropped = [d for f in files for d in f.get('dropped', [])]
        added = [d for f in files for d in f.get('added', [])]
        urls = ', '.join(sorted({f['url'] for f in files}))
        refresh = ('\n### Keyring update\n\n`%%openpgpverify` rejected the signature with '
                   'the keyring in dist-git (%s), while %s ignores that. %s has updated '
                   'the key since: the copy at %s %s and verifies the release with sqv. This '
                   'PR replaces the file with that copy, byte for byte%s:\n\n```\n%s\n```\n\n'
                   'Fingerprints%s:\n\n%s\n\n%sWhat changed in the certificate (`sq '
                   'inspect`):\n\n```diff\n%s```\n'
                   % (reason, old_tool,
                      'The key owner' if 'keys.openpgp.org' in urls else 'Upstream', urls,
                      'holds only the signing key' if dropped else
                      'has the same fingerprint(s) and also holds other keys upstream publishes '
                      'there' if added else 'has the same fingerprint(s)',
                      '' if not any(f.get('new_file') for f in files) else
                      ', named like the URL, which becomes its `Source`',
                      '\n'.join(c for f in files for c in f['commands']),
                      ' (kept)' if dropped else ' (unchanged)',
                      '\n'.join('- `%s`' % fp for f in files for fp in f['fingerprints']),
                      ('Dropped from the keyring (not used for the current release; add them '
                       'back if releases may be signed with them):\n\n%s\n\n'
                       % '\n'.join('- `%s`' % d for d in dropped)) if dropped else
                      ('Added to the keyring, because upstream\'s file holds them too; this '
                       'also means a release signed with one of them will verify:\n\n%s\n\n'
                       % '\n'.join('- `%s`' % d for d in added)) if added else '',
                      ''.join(diffs)))
    elif files:
        refresh = ('\n### Keyring refresh\n\n%sThe same certificate, looked up '
                   'by fingerprint (%s), has self-signatures our copy is missing (a renewed '
                   'expiry, modern hashes or the older binding history), so this PR replaces '
                   'the keyring with the keyserver copy. No key was added or removed. Please check the fingerprint '
                   'against upstream:\n\n%s\n\n%sWhat changed in the certificate (`sq '
                   'inspect`):\n\n```diff\n%s```\n'
                   % (('`%%openpgpverify` cannot read the keyring in dist-git: it is a GnuPG '
                       'keybox, which %s reads but sqv does not, so it is replaced with a '
                       'plain OpenPGP keyring. ' % old_tool) if keybox else
                      ('`%%openpgpverify` rejected the signature with the keyring in dist-git '
                       '(%s), while %s ignores that. ' % (reason, old_tool)),
                      '; '.join(sorted({v for f in files for v in f['found_via']})),
                      '\n'.join('- `%s`' % fp for f in files for fp in f['fingerprints']),
                      ''.join('The refresh, as run (the spec comment above the `Source` line '
                              'has the same command, for the next refresh):\n\n```\n%s\n'
                              '```\n\n' % '\n'.join(f['commands'])
                              for f in files if f.get('commands')),
                      ''.join(diffs)))
    for f in sigs:
        refresh += ('\n### New release signature\n\nThe updated self-signatures are newer than '
                    'the original release signature, and sqv requires the key to have been '
                    'validly bound when the signature was made, so the old signature still '
                    'fails with the refreshed keyring. Upstream made the release signature '
                    'again with the updated key, so `%s` is replaced with the new one from %s '
                    '(%s). It verifies with the refreshed keyring; the tarball itself is '
                    'unchanged.\n' % (f['file'], f['url'], '; '.join(
                        '%s, made %s, by `%s`' % (x['hash'], x['created'], x['issuer'])
                        for x in f['signatures'])))
    if s.get('bug_id') and (files or sigs):
        refresh += ('\nThis fixes [rhbz#%d](https://bugzilla.redhat.com/show_bug.cgi?id=%d), '
                    'filed for the failing check.\n' % (s['bug_id'], s['bug_id']))
    if files and kr.get('pr_note'):
        refresh += '\n' + kr['pr_note'] + '\n'
    if files:
        refresh += ('\nThe keyring change is the first of the two commits, so it can be '
                    'reviewed or merged on its own.\n')
    notes = ['- Rawhide only. Whether to merge it into other branches is up to you; '
             'openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10' +
             ('. It is not in EPEL 8, so if this spec is still used there, keep '
              '`%gpgverify` on that branch.' if s.get('rhel_conditional') else '.')]
    chk = s.get('gnupg2_check')
    if chk and chk['verdict'] == 'drop' and chk.get('unchecked'):
        notes.append('- `BuildRequires: gnupg2` is dropped too, without a full build: %s. '
                     'Nothing in the spec uses gpg besides the signature check. If the build '
                     'turns out to need it, it can come back.'
                     % (chk.get('why') or 'the sources are too large for the test machine'))
    elif chk and chk['verdict'] == 'drop' and chk.get('overridden'):
        notes.append('- `BuildRequires: gnupg2` is dropped too. The changed spec was built '
                     'completely (`rpmbuild -bb`%s) in a chroot with gnupg2 and gpgverify '
                     'removed, and the build passed. The build log or test files mention gpg '
                     '(%s), so tests that use gpg may now be skipped.'
                     % (', including `%check`' if chk.get('has_check') else '',
                        '; '.join('`%s`' % ' '.join(h.split()) for h in
                                  (chk.get('log_hits') or [])[:2]) or 'in the sources'))
    elif chk and chk['verdict'] == 'drop':
        notes.append('- `BuildRequires: gnupg2` is dropped too. To check that nothing else '
                     'needs it, the changed spec was built completely (`rpmbuild -bb`%s) in '
                     'a chroot with gnupg2 and gpgverify removed, and %s.'
                     % ((', including `%check`', 'neither the build log nor the test files '
                         'in the sources mention gpg') if chk.get('has_check') else
                        ('; the spec has no `%check`', 'the build log doesn\'t mention gpg')))
    elif chk:
        reason = ' '.join(chk['reason'].split())
        notes.append('- `BuildRequires: gnupg2` is kept%s.%s' % (
            '; whether it can go was not checked: ' + reason[len('not checked: '):]
            if reason.startswith('not checked: ') else ': ' + reason,
            ' If it was only there for the signature check, it can go too.'
            if reason.startswith('not checked') else
            ' It stays for what the build itself does with gpg; the source signature check '
            'no longer uses it.' if reason.startswith('the build fails without') else ''))
    elif s.get('gnupg2_action') in ('review', 'keep'):
        notes.append('- `BuildRequires: gnupg2` is kept: the spec has a `%check` section '
                     'or uses gpg elsewhere, and tests may need it. If it was only there '
                     'for the signature check, it can go too.')
    notes.append('- Nothing changes in the built packages, so this doesn\'t need a build '
                 'right away; the new check runs with your next build.')
    if s.get('stage') and s['stage'] != '-bp':
        notes.append('- The verification runs outside `%prep`. Moving it to the start of '
                     '`%prep` would check the sources before anything else uses them.')
    # Rebased onto a newer dist-git commit without re-running Phase 1 (the
    # maintainers' CI builds it).
    rebased = '' if not s.get('tested_commit') else (
        ' The spec has changed since (`%s`); this PR '
        'applies the same change on top of that without re-running the test, so the '
        'CI build here is the check for the current spec.' % s['spec_commit'][:12])
    if s.get('convert_untested'):
        result_old = result_new = 'no call (the check is off, see below)'
        rebased += ('\n\n**The signature check itself is not tested:** %s The conversion is '
                    'the same as in the other PRs for the Change, so the check works when it '
                    'runs again; the build above only shows that the spec still builds.'
                    % s['convert_untested'])
    text = tmpl('pr-description.md',
                changes='\n'.join(changes) + '\n', stage='rpmbuild %s' % s.get('stage', '-bp'),
                chroots=', '.join(chroots), old_tool=old_tool,
                intro_from='a direct GnuPG call (%s)' % old_tool if raw else
                '`%gpgverify` (GnuPG `gpgv`)',
                intro_tail='The spec called GnuPG itself instead of using `%gpgverify`; the '
                'check becomes one `%openpgpverify` call with the same keyring, signature '
                'and data.' if raw else
                'The macro takes the same options, so the call itself only changes its name.', calls_old=n_old, calls_new=calls_new,
                result_old=result_old, result_new=result_new,
                tested_on=(s.get('tested_at') or s['updated'])[:10],
                commit=(s.get('tested_commit') or s['spec_commit'])[:12],
                sqv_version=s.get('sqv_version') or '?', rebased_note=rebased,
                refresh_section=refresh,
                notes_section='\n### Notes\n\n' + '\n'.join(notes) + '\n')
    # No verification call ran (convert_untested): no sqv version to name.
    text = text.replace(' with sequoia-sqv ? (Fedora DEFAULT crypto policy)', '')
    title = 'Verify source signatures with openpgpverify'
    if draft:
        text = ('> **DRAFT, not to be opened yet:** the keyring refresh below still needs '
                'a human review (`scripts/refresh_keys.py show %s`).\n\n' % pkg) + text
    return patch, '# %s\n\n%s' % (title, text)


def render_bug(pkg, s):
    res = s['results'][0]
    bad = [c for c in res.get('new_calls', []) if c['rc'] != 0][0]
    # bug_reason: set by hand where the first error hides a second one.
    # bug_reason and bug_findings come from scripts/bug_diag.py (all problems).
    reason = s.get('bug_reason') or res.get('failure_reason')
    excerpt = sqv_excerpt(res.get('log_tail', ''))
    diag = s.get('bug_findings')
    if not diag and reason == 'sha1-sig' and re.search(r'(Certification|Binding)\) requiring',
                                                       excerpt):
        reason = 'sha1-sig-and-cert'
    short, why, actions = REASONS.get(reason) or GENERIC
    if diag:
        why = diag
    elif reason == 'sha1-sig' and 'No binding signature at time' in excerpt:
        why += (' The keyring in dist-git also has no self-signature from before the '
                'release signature, which is what sqv reports first above; a new '
                'signature with SHA-256 fixes both.')
    if s.get('bug_spec_comment'):
        why = ('The spec already says so (`%s`); this bug tracks it for the Change.\n\n'
               % s['bug_spec_comment']) + why
    kr = s.get('keyring_refresh') or {}
    if not diag and kr.get('status') in ('no-update', 'not-found') and reason not in (
            'sha1-cert', 'expired', 'binding-after-signature', 'v3-key-sha1-cert',
            'sha1-sig-and-cert'):
        why += ' (A refreshed key from keyservers/WKD doesn\'t help either.)'
    if s.get('raw_rewritten'):
        tools = sorted({c['tool'] for c in res.get('old_calls', [])} - {'gpgverify'})
        old_check = 'the current check with %s' % (
            ', '.join('`%s`' % x for x in tools) or 'GnuPG')
        actions = actions.replace('keep `%gpgverify`', 'keep the current GnuPG check')
        why = why.replace('`%gpgverify`', 'the current GnuPG check')
        spec_change = ('the spec change replaces the direct GnuPG call with one '
                       '`%{openpgpverify}` call (same keyring, signature and data) and adds '
                       '`BuildRequires: openpgpverify`; it is ready and tested up to the '
                       'signature check.')
    else:
        old_check = '`%gpgverify`'
        spec_change = ('the spec change is the same as for other packages: `%{gpgverify}` → '
                       '`%{openpgpverify}` and `BuildRequires: openpgpverify`.')
    return tmpl('bug.md', package=pkg, reason_short=short, commit=s['spec_commit'][:12],
                old_check=old_check, spec_change=spec_change,
                call='%%openpgpverify %s' % short_args(bad['args']),
                log_excerpt=excerpt, reason_text=why,
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
        if s and s.get('existing_prs'):
            index.append((pkg, 'skipped', 'open PR exists: %s' % ' '.join(s['existing_prs'])))
            continue
        status = (s or {}).get('status')
        if status not in ('tested', 'regression'):
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
            try:
                patch, text = render_pr(pkg, s, draft)
            except RuntimeError as e:
                shutil.rmtree(d, ignore_errors=True)
                index.append((pkg, 'skipped', str(e).split(': ', 1)[-1]))
                print('%-24s %s' % (pkg, index[-1][1]), flush=True)
                continue
            for name, text_ in split_series(patch):
                with open(os.path.join(d, name), 'w', newline='', errors='surrogateescape') as fh:
                    fh.write(text_)
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
             '- **PR**: `*.patch` are the commits a PR would carry (`git am` applies them '
             'to dist-git at the tested commit; a keyring update is a separate first '
             'commit); `PR.md` is the PR title and description.',
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
