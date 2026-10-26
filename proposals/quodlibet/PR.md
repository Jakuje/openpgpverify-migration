# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show quodlibet`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- refreshed keyring `E0AA0F031DBD80FFBA57B06D5A62D0CAB6264964` (see below)

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-26 at dist-git commit `1ee9e3f025d9` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `0EBF782C5D53F7E5FB02A66746BD761F7A49B0EC`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/E0AA0F031DBD80FFBA57B06D5A62D0CAB6264964
+++ refreshed/E0AA0F031DBD80FFBA57B06D5A62D0CAB6264964
@@ -1,15 +1,16 @@
       Fingerprint: 0EBF782C5D53F7E5FB02A66746BD761F7A49B0EC
-                   Invalid: The primary key is not live: Expired on 2025-01-25T13:44:38Z
-  Expiration time: 2025-01-25 13:44:38 UTC (creation time + 10years 8days 7h 24m 24s)
+  Expiration time: 2027-02-21 09:31:04 UTC (creation time + 12years 1month 4days 4h 37m 14s)
         Key flags: certification, signing
            Subkey: E0AA0F031DBD80FFBA57B06D5A62D0CAB6264964
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-01-25T13:44:38Z
-  Expiration time: 2025-01-25 13:45:33 UTC (creation time + 10years 8days 7h 21m 30s)
+  Expiration time: 2027-02-21 09:31:56 UTC (creation time + 12years 1month 4days 4h 34m 17s)
         Key flags: signing
            Subkey: BCC7A7AF77B2C37FC3E3867A0322E8C1C947D756
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-01-25T13:44:38Z
-  Expiration time: 2025-01-25 13:44:58 UTC (creation time + 10years 8days 7h 24m 44s)
+  Expiration time: 2027-02-21 09:31:30 UTC (creation time + 12years 1month 4days 4h 37m 40s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Christoph Reiter <reiter.christoph@gmail.com>
-self-signatures PositiveCertification: 2015-01-17, 2016-01-05, 2017-01-06, 2018-01-03, 2018-12-26, 2020-01-23, 2021-01-24, 2022-01-24, 2023-01-27, 2024-01-26
-self-signatures SubkeyBinding: 2015-01-17, 2016-01-05, 2017-01-06, 2018-01-03, 2018-12-26, 2020-01-23, 2021-01-24, 2022-01-24, 2023-01-27, 2024-01-26
+self-signatures PositiveCertification: 2015-01-17, 2016-01-05, 2017-01-06, 2018-01-03, 2018-12-26, 2020-01-23, 2021-01-24, 2022-01-24, 2023-01-27, 2024-01-26, 2025-02-09, 2026-02-21
+self-signatures SubkeyBinding: 2015-01-17, 2016-01-05, 2017-01-06, 2018-01-03, 2018-12-26, 2020-01-23, 2021-01-24, 2022-01-24, 2023-01-27, 2024-01-26, 2025-02-09, 2026-02-21
+third-party CasualCertification: 4
+third-party CertificationRevocation: 2
+third-party GenericCertification: 11
+third-party PositiveCertification: 1
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the changed spec does not get past the signature check. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
