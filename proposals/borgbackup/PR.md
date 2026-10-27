# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show borgbackup`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- refreshed keyring `gpgkey-6D5B_EF9A_DD20_7580_5747_B70F_9F88_FB52_FAF7_B393.gpg` (see below); the comment above its `Source` line now shows the commands for refreshing it
- Release bumped (`1%{?dist}` → `2%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-26 at dist-git commit `d2613c8484b3` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `6D5BEF9ADD2075805747B70F9F88FB52FAF7B393`

The refresh, as run (the spec comment above the `Source` line has the same commands, for the next refresh):

```
sq --home=none network search --output - 6D5BEF9ADD2075805747B70F9F88FB52FAF7B393 \
  | sq keyring filter --experimental --cert 6D5BEF9ADD2075805747B70F9F88FB52FAF7B393 --output update.pgp
sq keyring merge gpgkey-6D5B_EF9A_DD20_7580_5747_B70F_9F88_FB52_FAF7_B393.gpg update.pgp | sq packet dearmor --output gpgkey-6D5B_EF9A_DD20_7580_5747_B70F_9F88_FB52_FAF7_B393.gpg.new
mv gpgkey-6D5B_EF9A_DD20_7580_5747_B70F_9F88_FB52_FAF7_B393.gpg.new gpgkey-6D5B_EF9A_DD20_7580_5747_B70F_9F88_FB52_FAF7_B393.gpg
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/gpgkey-6D5B_EF9A_DD20_7580_5747_B70F_9F88_FB52_FAF7_B393.gpg
+++ refreshed/gpgkey-6D5B_EF9A_DD20_7580_5747_B70F_9F88_FB52_FAF7_B393.gpg
@@ -1,22 +1,25 @@
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
+third-party CasualCertification: 15
+third-party GenericCertification: 52
+third-party PositiveCertification: 25
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the changed spec does not get past the signature check. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
