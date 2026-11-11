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
- refreshed keyring `coreutils-keyring.gpg` (see below)
- replaced the release signature `coreutils-9.12.tar.xz.sig` with the one upstream made again with the updated key (see below); it was in the lookaside cache, which a PR cannot update, so it moves into git (its line in `sources` is dropped)
- Release bumped (`1%{?dist}` → `2%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | pass |

Tested on 2026-11-11 at dist-git commit `072fa66649a4` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (SHA-1 key self-signatures), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR replaces the keyring with the keyserver copy. No key was added or removed. Please check the fingerprint against upstream:

- `6C37DC12121A5006BC1DB804DF6FD971306037D9`

The refresh, as run (the spec comment above the `Source` line has the same command, for the next refresh):

```
sq --home=none network keyserver search 6C37DC12121A5006BC1DB804DF6FD971306037D9 --output coreutils-keyring.gpg --overwrite
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/coreutils-keyring.gpg
+++ refreshed/coreutils-keyring.gpg
@@ -1,19 +1,14 @@
       Fingerprint: 6C37DC12121A5006BC1DB804DF6FD971306037D9
-                   Invalid: No binding signature at time 2026-11-11T10:29:18Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: 5B39036B3C18C1DDB9D1FF4DDBF3EE043A2713EB
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-11T10:29:18Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Pádraig Brady <P@draigBrady.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Pádraig Brady <pbrady@redhat.com>
-                   Invalid: No binding signature at time 2026-11-11T10:29:18Z
-           UserID: Pádraig Brady <pixelbeat@gnu.org>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
+           UserID: Pádraig Brady <pixelbeat@gnu.org>
 self-signatures CertificationRevocation: 2016-01-20
-self-signatures PositiveCertification: 2011-09-23
-self-signatures SubkeyBinding: 2011-09-23
+self-signatures PositiveCertification: 2011-09-23, 2026-11-09
+self-signatures SubkeyBinding: 2011-09-23, 2026-11-09
 third-party GenericCertification: 2
 third-party PositiveCertification: 7
```

### New release signature

The updated self-signatures are newer than the original release signature, and sqv requires the key to have been validly bound when the signature was made, so the old signature still fails with the refreshed keyring. Upstream made the release signature again with the updated key, so `coreutils-9.12.tar.xz.sig` is replaced with the new one from https://bugzilla.redhat.com/attachment.cgi?id=2163199 (SHA512, made 2026-11-09 14:45:30, by `6C37DC12121A5006BC1DB804DF6FD971306037D9`). It verifies with the refreshed keyring; the tarball itself is unchanged.

This fixes [rhbz#2569053](https://bugzilla.redhat.com/show_bug.cgi?id=2569053), filed for the failing check.

The new signature is the one upstream attached to [rhbz#2569053](https://bugzilla.redhat.com/show_bug.cgi?id=2569053) (attachment 2163199). ftp.gnu.org still serves the original `coreutils-9.12.tar.xz.sig`, so the file named by the `Source1` URL differs from the one in git until upstream replaces it there; the next release will be signed with the updated key anyway.

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is dropped too. To check that nothing else needs it, the changed spec was built completely (`rpmbuild -bb`, including `%check`) in a chroot with gnupg2 and gpgverify removed, and neither the build log nor the test files in the sources mention gpg.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
