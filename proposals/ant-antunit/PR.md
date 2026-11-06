# Verify source signatures with openpgpverify

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- dropped `BuildRequires:  gnupg2`, only needed for `%gpgverify`
- converted upstream's KEYS file into the keyring `KEYS.pgp`, which the `Source` line now names (see below); the comment above its `Source` line shows the commands
- `KEYS` is no longer used; its line in `sources` is dropped

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | pass |

Tested on 2026-11-06 at dist-git commit `be99ed541961` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` cannot use upstream's KEYS file: it holds 2 v3 (PGP 2) keys, which Sequoia does not parse, so sqv rejects the whole file (GnuPG skips such keys silently). This PR converts it with GnuPG into `KEYS.pgp`, a plain OpenPGP keyring. It keeps every key GnuPG reads from the KEYS file (19 certificates), so releases by any of the release managers listed there keep verifying. Exactly these commands (also in the comment above the keyring's `Source` line, for the next update):

```
curl -fsSL -O https://archive.apache.org/dist/ant/KEYS
GNUPGHOME="$(mktemp -d)" sh -c 'gpg --batch --import KEYS; gpg --batch --export --output KEYS.pgp'
rm KEYS
```

The current release is signed by:

- `BC26C53AF531F8B4B3F5930AAFBD3AF8EAFA72DA`

Another way to fix this would be to keep only the key that signed the current release, pulled from keyservers (`sq network keyserver search FINGERPRINT --output keyring.pgp`). That keyring is much smaller, but it would need another update whenever a different release manager signs a release, so this PR keeps all the keys from KEYS.

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is dropped too. To check that nothing else needs it, the changed spec was built completely (`rpmbuild -bb`, including `%check`) in a chroot with gnupg2 and gpgverify removed, and neither the build log nor the test files in the sources mention gpg.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
