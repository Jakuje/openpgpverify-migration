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
- updated `ntpsec.gpg.pub.asc` to the current upstream copy from the URL in the spec (see below)
- Release bumped (`1%{?dist}` → `2%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | pass |

Tested on 2026-11-05 at dist-git commit `4d9ab763e0d2` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (verification fails), while `%gpgverify` ignores that. Upstream has updated the key since: the copy at https://ftp.ntpsec.org/pub/releases/ntpsec.gpg.pub.asc has the same fingerprint(s) and also holds other keys upstream publishes there and verifies the release with sqv. This PR replaces the file with that copy, byte for byte:

```
curl -fsSL -O https://ftp.ntpsec.org/pub/releases/ntpsec.gpg.pub.asc
```

Fingerprints (unchanged):

- `DA3FDF774CC70FA64729EC4505D9B371477C7528`
- `E57235D22764129FA4F2F4D17F52608ED0E49D76`

Added to the keyring, because upstream's file holds them too; this also means a release signed with one of them will verify:

- `B48237761A2690222C995F445A22E330161C3978`
- `B09A8CABE180EC664CC511D82A7C3E36CC282DBE`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/ntpsec.gpg.pub.asc
+++ upstream/ntpsec.gpg.pub.asc
@@ -3,16 +3,34 @@
         Key flags: certification, signing
            Subkey: F1B3A359ACD57A7BFE493ABFAE3C53420F49D2EF
         Key flags: transport encryption, data-at-rest encryption
+           UserID: NTPsec Contact <contact@ntpsec.org>
            UserID: NTPsec Security Reporting <security@ntpsec.org>
+      Fingerprint: B48237761A2690222C995F445A22E330161C3978
+                   Invalid: Policy rejected asymmetric algorithm: DSA3072 is not considered secure
+           Subkey: EA43F260ED749264A5201D8B6D4A4A63C5A6BB27
+                   Invalid: primary key: Policy rejected asymmetric algorithm, because DSA3072 is not considered secure
+           UserID: NTPsec Contact <contact@ntpsec.org>
+           UserID: NTPsec Security Reporting <security@ntpsec.org>
+      Fingerprint: B09A8CABE180EC664CC511D82A7C3E36CC282DBE
+                   Revoked:
+                      Message: Revoked by Mark Atwood <mark.atwood@ntpsec.org>
+                   Invalid: No binding signature at time 2026-11-05T09:38:26Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+           Subkey: 9DB7FAFCF3545F14EF77AB765B56609E99556C0E
+                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
+                   Invalid: primary key: No binding signature at time 2026-11-05T09:38:26Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+           UserID: NTPsec Security Reporting <security@ntpsec.org>
+                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
       Fingerprint: E57235D22764129FA4F2F4D17F52608ED0E49D76
-                   Invalid: The primary key is not live: Expired on 2025-10-05T04:11:25Z
-  Expiration time: 2025-10-05 04:11:25 UTC (creation time + 4years 11months 29days 3h 50m 24s)
+  Expiration time: 2028-07-30 04:21:41 UTC (creation time + 7years 9months 23days 7h 7m 52s)
         Key flags: certification, signing
            Subkey: 4068094035426D1F8F8AA800F8FE4D92CC4090B5
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-10-05T04:11:25Z
-  Expiration time: 2025-10-05 04:11:25 UTC (creation time + 4years 11months 29days 3h 50m 24s)
+  Expiration time: 2028-07-30 04:23:52 UTC (creation time + 7years 9months 23days 7h 10m 3s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: NTPsec Security Reporting <security@ntpsec.org>
-self-signatures PositiveCertification: 2016-04-14, 2020-10-06
-self-signatures SubkeyBinding: 2020-10-06
-third-party GenericCertification: 1
+self-signatures GenericCertification: 2016-04-14
+self-signatures KeyRevocation: 2016-04-14
+self-signatures PositiveCertification: 2015-09-29, 2016-04-14, 2017-02-22, 2018-06-08, 2020-10-06, 2026-07-31
+self-signatures SubkeyBinding: 2015-09-29, 2016-04-14, 2018-06-08, 2020-10-06, 2026-07-31
+third-party GenericCertification: 4
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is dropped too. To check that nothing else needs it, the changed spec was built completely (`rpmbuild -bb`, including `%check`) in a chroot with gnupg2 and gpgverify removed, and neither the build log nor the test files in the sources mention gpg.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
