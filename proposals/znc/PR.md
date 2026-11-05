# Verify source signatures with openpgpverify

This switches the upstream source signature check from a direct GnuPG call (`gpg2`, `gpgv2`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The spec called GnuPG itself instead of using `%gpgverify`; the check becomes one `%openpgpverify` call with the same keyring, signature and data.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- the GnuPG verification (temporary home, dearmored key, `gpgv2`, cleanup) is replaced by one `%{openpgpverify}` call with the same key, signature and data; sqv reads the armored key directly and uses no home directory
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- dropped `BuildRequires:  gnupg2`, only needed for the GnuPG verification
- refreshed keyring `gpgkey-5AE420CC0209989E.asc` (see below)
- Release bumped (`1%{?dist}` → `2%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64, fedora-eln-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`gpg2`, `gpgv2`) | 2 | pass |
| this PR (`%openpgpverify`) | 1 | pass |

Tested on 2026-11-05 at dist-git commit `cae0b85cca65` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (verification fails), while `gpg2`, `gpgv2` ignores that. The same certificate, looked up by fingerprint (hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR replaces the keyring with the keyserver copy. No key was added or removed. Please check the fingerprint against upstream:

- `D5823CACB477191CAC0075555AE420CC0209989E`

The refresh, as run (the spec comment above the `Source` line has the same command, for the next refresh):

```
sq --home=none network keyserver search D5823CACB477191CAC0075555AE420CC0209989E --output gpgkey-5AE420CC0209989E.asc --overwrite
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/gpgkey-5AE420CC0209989E.asc
+++ refreshed/gpgkey-5AE420CC0209989E.asc
@@ -1,21 +1,19 @@
       Fingerprint: D5823CACB477191CAC0075555AE420CC0209989E
-                   Invalid: No binding signature at time 2026-11-05T18:20:33Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2030-02-17 23:55:54 UTC (creation time + 18years 3months 9days 12h 24m 10s)
+        Key flags: certification, signing
            Subkey: A1951C9AE193C618F082AE7F17611B1A40BDEDED
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-05T18:20:33Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2030-02-17 23:55:36 UTC (creation time + 18years 3months 9days 12h 23m 52s)
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Alexey Sokolov (ZNC) <alexey+znc@asokolov.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
+           UserID: Alexey Sokolov <alexey+gentoo@asokolov.org>
            UserID: Alexey Sokolov <alexey@alexeysokolov.co.cc>
                    Revoked:
-                   Invalid: No binding signature at time 2026-11-05T18:20:33Z
-           UserID: Alexey Sokolov <alexey@asokolov.org>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
+           UserID: Alexey Sokolov <alexey@asokolov.org>
            UserID: Alexey Sokolov <ktonibud@gmail.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
+           UserID: Alexey Sokolov <sokolov@google.com>
 self-signatures CertificationRevocation: 2015-12-09
-self-signatures PositiveCertification: 2017-01-08
-self-signatures SubkeyBinding: 2017-01-08
+self-signatures PositiveCertification: 2011-11-09, 2013-06-09, 2013-11-04, 2016-08-27, 2017-01-08, 2019-12-23, 2020-05-24, 2022-12-25, 2025-02-18
+self-signatures SubkeyBinding: 2011-11-09, 2013-06-09, 2016-08-27, 2017-01-08, 2019-12-23, 2022-12-25, 2025-02-18
+third-party GenericCertification: 1
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is dropped too. To check that nothing else needs it, the changed spec was built completely (`rpmbuild -bb`; the spec has no `%check`) in a chroot with gnupg2 and gpgverify removed, and the build log doesn't mention gpg.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
