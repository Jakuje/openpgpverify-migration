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
- refreshed keyring `gpgkey-B818B9CADF9089C2D5CEC66B75AD65802A0B4211.asc` (see below)
- replaced the release signature `libtpms-0.10.2.tar.gz.asc` with the one upstream made again with the updated key (see below); it was in the lookaside cache, which a PR cannot update, so it moves into git (its line in `sources` is dropped)
- Release bumped (`5%{?dist}` → `6%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | pass |

Tested on 2026-11-11 at dist-git commit `ccc54eaed99d` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (SHA-1 key self-signatures), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR replaces the keyring with the keyserver copy. No key was added or removed. Please check the fingerprint against upstream:

- `B818B9CADF9089C2D5CEC66B75AD65802A0B4211`

The refresh, as run (the spec comment above the `Source` line has the same command, for the next refresh):

```
sq --home=none network keyserver search B818B9CADF9089C2D5CEC66B75AD65802A0B4211 --output gpgkey-B818B9CADF9089C2D5CEC66B75AD65802A0B4211.asc --overwrite
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/gpgkey-B818B9CADF9089C2D5CEC66B75AD65802A0B4211.asc
+++ refreshed/gpgkey-B818B9CADF9089C2D5CEC66B75AD65802A0B4211.asc
@@ -1,6 +1,7 @@
       Fingerprint: B818B9CADF9089C2D5CEC66B75AD65802A0B4211
-                   Invalid: No binding signature at time 2026-11-11T10:28:53Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2027-10-02 15:51:34 UTC (creation time + 9years 11months 27days 21h 50m 24s)
+        Key flags: certification, signing
+           UserID: Stefan Berger <stefanb@linux.ibm.com>
            UserID: Stefan Berger <stefanb@linux.vnet.ibm.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2017-10-04
+self-signatures PositiveCertification: 2017-10-04, 2026-11-10
+third-party GenericCertification: 1
```

### New release signature

The updated self-signatures are newer than the original release signature, and sqv requires the key to have been validly bound when the signature was made, so the old signature still fails with the refreshed keyring. Upstream made the release signature again with the updated key, so `libtpms-0.10.2.tar.gz.asc` is replaced with the new one from https://github.com/stefanberger/libtpms/releases/download/v0.10.2/v0.10.2.tar.gz.asc (SHA512, made 2026-11-10 19:42:57, by `B818B9CADF9089C2D5CEC66B75AD65802A0B4211`). It verifies with the refreshed keyring; the tarball itself is unchanged.

This fixes [rhbz#2569338](https://bugzilla.redhat.com/show_bug.cgi?id=2569338), filed for the failing check.

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is dropped too. To check that nothing else needs it, the changed spec was built completely (`rpmbuild -bb`, including `%check`) in a chroot with gnupg2 and gpgverify removed, and neither the build log nor the test files in the sources mention gpg.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
