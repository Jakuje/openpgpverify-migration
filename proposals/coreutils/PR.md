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
- dropped `BuildRequires: gnupg2`, only needed for `%gpgverify`
- updated `coreutils-keyring.gpg` to the current upstream copy from the URL in the spec (see below)
- replaced the release signature `coreutils-9.12.tar.xz.sig` with the one upstream made again with the updated key (see below); it was in the lookaside cache, which a PR cannot update, so it moves into git (its line in `sources` is dropped)
- Release bumped (`1%{?dist}` → `2%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | pass |

Tested on 2026-11-16 at dist-git commit `072fa66649a4` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (SHA-1 key self-signatures), while `%gpgverify` ignores that. Upstream has updated the key since: the copy at https://savannah.gnu.org/project/release-gpgkeys.php?group=coreutils&download=1 has the same fingerprint(s) and verifies the release with sqv. This PR replaces the file with that copy, byte for byte:

```
curl -fsSL -o coreutils-keyring.gpg 'https://savannah.gnu.org/project/release-gpgkeys.php?group=coreutils&download=1'
```

Fingerprints (unchanged):

- `6C37DC12121A5006BC1DB804DF6FD971306037D9`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/coreutils-keyring.gpg
+++ upstream/coreutils-keyring.gpg
@@ -1,19 +1,11 @@
       Fingerprint: 6C37DC12121A5006BC1DB804DF6FD971306037D9
-                   Invalid: No binding signature at time 2026-11-16T10:30:13Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: 5B39036B3C18C1DDB9D1FF4DDBF3EE043A2713EB
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-16T10:30:13Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Pádraig Brady <P@draigBrady.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Pádraig Brady <pbrady@redhat.com>
                    Invalid: No binding signature at time 2026-11-16T10:30:13Z
            UserID: Pádraig Brady <pixelbeat@gnu.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
 self-signatures CertificationRevocation: 2016-01-20
-self-signatures PositiveCertification: 2011-09-23
-self-signatures SubkeyBinding: 2011-09-23
-third-party GenericCertification: 2
-third-party PositiveCertification: 7
+self-signatures PositiveCertification: 2026-11-09
+self-signatures SubkeyBinding: 2026-11-09
```

### New release signature

The updated self-signatures are newer than the original release signature, and sqv requires the key to have been validly bound when the signature was made, so the old signature still fails with the refreshed keyring. Upstream made the release signature again with the updated key, so `coreutils-9.12.tar.xz.sig` is replaced with the new one from https://bugzilla.redhat.com/attachment.cgi?id=2163199 (SHA512, made 2026-11-09 14:45:30, by `6C37DC12121A5006BC1DB804DF6FD971306037D9`). It verifies with the refreshed keyring; the tarball itself is unchanged.

This fixes [rhbz#2569053](https://bugzilla.redhat.com/show_bug.cgi?id=2569053), filed for the failing check.

The new signature is the one upstream attached to [rhbz#2569053](https://bugzilla.redhat.com/show_bug.cgi?id=2569053) (attachment 2163199). Upstream prefers not to replace files on ftp.gnu.org ([comment 4](https://bugzilla.redhat.com/show_bug.cgi?id=2569053#c4)), so the file named by the `Source1` URL differs from the one in git. 9.13, expected in about three weeks, will be signed with the updated key only; from then on the signature comes from ftp.gnu.org again and only the keyring change remains.

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is dropped too. To check that nothing else needs it, the changed spec was built completely (`rpmbuild -bb`, including `%check`) in a chroot with gnupg2 and gpgverify removed, and neither the build log nor the test files in the sources mention gpg.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
