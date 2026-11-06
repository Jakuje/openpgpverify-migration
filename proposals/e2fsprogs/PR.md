# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show e2fsprogs`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- replaced the keyring with the signing key from keyservers, keyring `tytso-key.asc` (see below); the comment above its `Source` line shows the commands
- Release bumped (`2%{?dist}` → `3%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64, fedora-eln-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-12 at dist-git commit `48612ca55f3c` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` cannot use the keyring in dist-git: it holds 2 v3 (PGP 2) keys, which Sequoia does not parse, so sqv rejects the whole file (GnuPG skips such keys silently). This PR replaces it with the keyserver copy of the key that signed the release, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), with exactly this command (also in the comment above the keyring's `Source` line, for the next update):

```
sq --home=none network keyserver search 3AB057B7E78D945C8C5591FBD36F769BC11804F0 --output tytso-key.asc --overwrite
```

Please check the fingerprint against upstream:

- `3AB057B7E78D945C8C5591FBD36F769BC11804F0`

Dropped from the keyring (not used for the current release; add them back if releases may be signed with them):

- `52C344D60D02CD9B07031447ED3A39E393674C40`
- `44140F903D4FC37F4082381B475FBA0D103D4013`

What changed in the signing certificate (`sq inspect`):

```diff
--- dist-git/tytso-key.asc (as GnuPG reads it)
+++ new/tytso-key.asc
@@ -1,44 +1,24 @@
-      Fingerprint: 52C344D60D02CD9B07031447ED3A39E393674C40
-                   Invalid: Policy rejected asymmetric algorithm: DSA1024 is not considered secure
-           Subkey: 3AF4690ED2AA4262A84008C5213F1DF8DB988C15
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: Policy rejected asymmetric algorithm, because DSA1024 is not considered secure
-           UserID: Theodore Y. Ts'o <tytso@mit.edu>
-      Fingerprint: 44140F903D4FC37F4082381B475FBA0D103D4013
-                   Invalid: No binding signature at time 2026-11-06T09:25:21Z: Policy rejected non-revocation signature (GenericCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: 57437BFAD7E46AB72A7C1168CBCACBC16963CE7A
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-06T09:25:21Z, because Policy rejected non-revocation signature (GenericCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Theodore Ts'o <tytso@valinux.com>
-                   Invalid: Policy rejected non-revocation signature (GenericCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
       Fingerprint: 3AB057B7E78D945C8C5591FBD36F769BC11804F0
         Key flags: certification, signing
            Subkey: 2B69B954DBFE0879288137C9F2F95956950D81A3
-                   Invalid: The subkey is not live: Expired on 2015-10-02T21:08:43Z
-  Expiration time: 2015-10-02 21:08:43 UTC (creation time + 6months 2days 10h 7m 6s)
+  Expiration time: 2027-10-14 23:44:14 UTC (creation time + 12years 6months 14days 12h 42m 37s)
         Key flags: signing
            Subkey: 8A238833A173C1DB60D59CCDF60754F903885799
-                   Invalid: The subkey is not live: Expired on 2015-10-02T21:09:03Z
-  Expiration time: 2015-10-02 21:09:03 UTC (creation time + 6months 2days 10h 4m 32s)
+  Expiration time: 2027-10-14 23:44:32 UTC (creation time + 12years 6months 14days 12h 40m 1s)
         Key flags: transport encryption, data-at-rest encryption
            Subkey: A1F769CA596F15CEDF652653D814B8F32F894C7A
         Key flags: transport encryption, data-at-rest encryption
            Subkey: A933CD6B33B9F4AF1C1144CA06259228B59ED8DF
         Key flags: authentication
            Subkey: C743E9AD1E36FDCCBF4E0EE9465BBB8C3E430766
-                   Invalid: The subkey is not live: Expired on 2015-10-02T21:09:17Z
-  Expiration time: 2015-10-02 21:09:17 UTC (creation time + 6months 2days 6h 40m 6s)
+  Expiration time: 2027-10-14 23:44:32 UTC (creation time + 12years 6months 14days 9h 15m 21s)
         Key flags: authentication
            UserID: Theodore Ts'o <tytso@debian.org>
            UserID: Theodore Ts'o <tytso@google.com>
            UserID: Theodore Ts'o <tytso@mit.edu>
-self-signatures GenericCertification: 1997-08-12, 1999-07-13, 2010-12-02
-self-signatures PositiveCertification: 2003-11-20, 2010-01-14, 2010-12-02, 2015-03-31
-self-signatures SubkeyBinding: 1997-08-12, 1999-07-13, 2010-12-02, 2014-01-29, 2015-07-04
-third-party CasualCertification: 22
-third-party GenericCertification: 170
+self-signatures PositiveCertification: 2010-12-02, 2015-03-31, 2026-04-22
+self-signatures SubkeyBinding: 2010-12-02, 2014-01-29, 2015-03-31, 2015-07-04, 2015-09-16, 2016-01-20, 2016-05-12, 2016-09-19, 2017-06-17, 2017-12-17, 2018-05-24, 2018-11-17, 2019-05-31, 2019-12-16, 2020-05-17, 2021-01-04, 2021-06-23, 2022-03-22, 2023-06-21, 2024-03-24, 2024-12-24, 2025-04-10, 2026-04-22
+third-party CasualCertification: 6
+third-party GenericCertification: 65
 third-party PersonaCertification: 1
-third-party PositiveCertification: 50
+third-party PositiveCertification: 8
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: the spec has a `%check` section or uses gpg elsewhere, and tests may need it. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
