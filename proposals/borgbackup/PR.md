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
- replaced keyring `gpgkey-6D5B_EF9A_DD20_7580_5747_B70F_9F88_FB52_FAF7_B393.gpg` with `gpgkey-6D5B_EF9A_DD20_7580_5747_B70F_9F88_FB52_FAF7_B393.asc` from https://keys.openpgp.org/vks/v1/by-fingerprint/6D5BEF9ADD2075805747B70F9F88FB52FAF7B393#/gpgkey-6D5B_EF9A_DD20_7580_5747_B70F_9F88_FB52_FAF7_B393.asc; its `Source` line is now that URL (see below)
- Release bumped (`1%{?dist}` → `2%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | pass |

Tested on 2026-11-05 at dist-git commit `d2613c8484b3` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (verification fails), while `%gpgverify` ignores that. The key owner has updated the key since: the copy at https://keys.openpgp.org/vks/v1/by-fingerprint/6D5BEF9ADD2075805747B70F9F88FB52FAF7B393#/gpgkey-6D5B_EF9A_DD20_7580_5747_B70F_9F88_FB52_FAF7_B393.asc has the same fingerprint(s) and verifies the release with sqv. This PR replaces the file with that copy, byte for byte, named like the URL, which becomes its `Source`:

```
curl -fsSL -o gpgkey-6D5B_EF9A_DD20_7580_5747_B70F_9F88_FB52_FAF7_B393.asc 'https://keys.openpgp.org/vks/v1/by-fingerprint/6D5BEF9ADD2075805747B70F9F88FB52FAF7B393'
```

Fingerprints (unchanged):

- `6D5BEF9ADD2075805747B70F9F88FB52FAF7B393`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/gpgkey-6D5B_EF9A_DD20_7580_5747_B70F_9F88_FB52_FAF7_B393.gpg
+++ upstream/gpgkey-6D5B_EF9A_DD20_7580_5747_B70F_9F88_FB52_FAF7_B393.gpg
@@ -1,22 +1,22 @@
       Fingerprint: 6D5BEF9ADD2075805747B70F9F88FB52FAF7B393
-                   Invalid: The primary key is not live: Expired on 2019-12-24T00:03:19Z
-  Expiration time: 2019-12-24 00:03:19 UTC (creation time + 9years 11months 27days 22h 38m 26s)
         Key flags: certification, signing
            Subkey: 2F81AFFBAB04E11FE8EE65D4243ACFA951F78E01
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2019-12-24T00:03:19Z
-  Expiration time: 2021-03-01 22:40:33 UTC (creation time + 6years 2months 6days 12h 11m 6s)
+  Expiration time: 2029-02-17 10:05:20 UTC (creation time + 14years 1month 24days 10h 9m 29s)
         Key flags: signing
+           Subkey: 3417BA7D795C88DAB6719915A28818512946B68A
+                   Invalid: The subkey is not live: Expired on 2014-12-26T01:25:06Z
+  Expiration time: 2014-12-26 01:25:06 UTC (creation time + 4years 11months 30days 5h 51m 19s)
+        Key flags: transport encryption, data-at-rest encryption
            Subkey: 42B4A35AC7754DC6EC29AFDB80D1C3A354D9A2EF
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2019-12-24T00:03:19Z
-  Expiration time: 2021-03-01 22:40:33 UTC (creation time + 6years 2months 6days 12h 9m 54s)
+  Expiration time: 2029-02-17 10:05:20 UTC (creation time + 14years 1month 24days 10h 8m 17s)
         Key flags: transport encryption, data-at-rest encryption
+           Subkey: 9FCB53A2E7DA4C088568C3FA90A8763631A6CB60
+                   Invalid: Policy rejected non-revocation signature (PrimaryKeyBinding) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
+                   Invalid: Policy rejected non-revocation signature (PrimaryKeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
            UserID: Thomas Waldmann <thomas.j.waldmann@gmail.com>
            UserID: Thomas Waldmann <tw-public@gmx.de>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Thomas Waldmann <tw@waldmann-edv.de>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Thomas Waldmann <twaldmann@thinkmo.de>
-self-signatures PositiveCertification: 2014-06-01, 2014-08-12
-self-signatures SubkeyBinding: 2019-03-02
+self-signatures PositiveCertification: 2009-12-26, 2014-06-01, 2014-08-12, 2020-01-06, 2021-02-14, 2022-02-15, 2024-02-15
+self-signatures SubkeyBinding: 2009-12-25, 2014-12-25, 2015-12-30, 2017-01-06, 2017-11-22, 2019-03-02, 2021-02-14, 2022-02-15, 2024-02-15, 2026-02-18
```

This copy is from keys.openpgp.org, looked up by fingerprint, so it is the same key the old file held. If the project publishes the key somewhere you prefer, that URL works as well, as long as the copy verifies this release.

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is dropped too. To check that nothing else needs it, the changed spec was built completely (`rpmbuild -bb`, including `%check`) in a chroot with gnupg2 and gpgverify removed, and neither the build log nor the test files in the sources mention gpg.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
