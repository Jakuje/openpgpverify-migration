# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show libidn2`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- refreshed keyring `B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE` (see below)
- Release bumped (`4%{?dist}` → `5%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-12 at dist-git commit `d30596280503` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.mailvelope.com, hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
+++ refreshed/B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
@@ -1,19 +1,17 @@
       Fingerprint: B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
-                   Invalid: The primary key is not live: Expired on 2022-10-23T15:48:28Z
-  Expiration time: 2022-10-23 15:48:28 UTC (creation time + 3years 7months 3days 20h 15m 52s)
+  Expiration time: 2026-11-19 08:55:45 UTC (creation time + 7years 8months 2h 49m 33s)
         Key flags: certification, signing
            Subkey: CA7E37164342DF3133DF349780260EE8A9B92B2B
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-10-23T15:48:28Z
-  Expiration time: 2022-10-23 15:48:43 UTC (creation time + 3years 7months 3days 20h 12m 54s)
+  Expiration time: 2026-11-18 07:59:19 UTC (creation time + 7years 7months 29days 12h 23m 30s)
         Key flags: authentication
            Subkey: A3CC9C870B9D310ABAD4CF2F51722B08FE4745A2
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-10-23T15:48:28Z
-  Expiration time: 2022-10-23 15:48:47 UTC (creation time + 3years 7months 3days 20h 12m 46s)
+  Expiration time: 2026-11-18 07:59:19 UTC (creation time + 7years 7months 29days 12h 23m 18s)
         Key flags: signing
            Subkey: A9EC8F4D7F1E50ED3DEF49A902923D7EE76EBD60
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-10-23T15:48:28Z
-  Expiration time: 2022-10-23 15:48:36 UTC (creation time + 3years 7months 3days 20h 12m 58s)
+  Expiration time: 2026-11-18 07:59:19 UTC (creation time + 7years 7months 29days 12h 23m 41s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Simon Josefsson <simon@josefsson.org>
-self-signatures PositiveCertification: 2019-03-20, 2019-10-23, 2020-05-27, 2020-12-22, 2021-07-21, 2022-03-21
-self-signatures SubkeyBinding: 2019-03-20, 2019-10-23, 2020-05-27, 2020-12-22, 2021-07-21, 2022-03-21
+self-signatures PositiveCertification: 2019-03-20, 2019-10-23, 2020-05-27, 2020-12-22, 2021-07-21, 2022-03-21, 2022-10-04, 2023-09-01, 2024-03-22, 2025-03-12, 2026-04-17
+self-signatures SubkeyBinding: 2019-03-20, 2019-10-23, 2020-05-27, 2020-12-22, 2021-07-21, 2022-03-21, 2022-10-04, 2023-09-01, 2024-03-22, 2025-03-12, 2026-04-16
+third-party GenericCertification: 7
+third-party PositiveCertification: 1
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is in Fedora 43 and later, but not in EPEL yet, so please keep `%gpgverify` on EPEL branches.
- `BuildRequires: gnupg2` is kept: the spec has a `%check` section or uses gpg elsewhere, and tests may need it. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
