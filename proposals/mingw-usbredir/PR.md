# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show mingw-usbredir`).

This switches the upstream source signature check from a direct GnuPG call (`gpgv2`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The spec called GnuPG itself instead of using `%gpgverify`; the check becomes one `%openpgpverify` call with the same keyring, signature and data.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- the direct `gpgv2` call is replaced by `%{openpgpverify}` with the same keyring, signature and data
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- `victortoso-E37A484F.keyring` was in the lookaside cache, which a PR cannot update, so it moves into git (its line in `sources` is dropped)
- refreshed keyring `victortoso-E37A484F.keyring` (see below); the comment above its `Source` line now shows the commands for refreshing it
- Release bumped (`6%{?dist}` → `7%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`gpgv2`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-26 at dist-git commit `707de3bf50de` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `gpgv2` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `206D3B352F566F3B0E6572E997D9123DE37A484F`

The refresh, as run (the spec comment above the `Source` line has the same commands, for the next refresh):

```
sq --home=none network search --output - 206D3B352F566F3B0E6572E997D9123DE37A484F \
  | sq keyring filter --experimental --cert 206D3B352F566F3B0E6572E997D9123DE37A484F --output update.pgp
sq keyring merge victortoso-E37A484F.keyring update.pgp | sq packet dearmor --output victortoso-E37A484F.keyring.new
mv victortoso-E37A484F.keyring.new victortoso-E37A484F.keyring
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/victortoso-E37A484F.keyring
+++ refreshed/victortoso-E37A484F.keyring
@@ -1,26 +1,25 @@
       Fingerprint: 206D3B352F566F3B0E6572E997D9123DE37A484F
-                   Invalid: The primary key is not live: Expired on 2019-07-03T10:40:12Z
-  Expiration time: 2019-07-03 10:40:12 UTC (creation time + 3years 4months 22days 11h 15m 15s)
+  Expiration time: 2027-01-28 10:25:47 UTC (creation time + 10years 11months 18days 15h 5m 38s)
         Key flags: certification, signing
            Subkey: 64EE94DD16CF2DECEBCFA62BE98F5B4819679A78
-                   Revoked:
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2019-07-03T10:40:12Z
-  Expiration time: 2017-03-12 21:56:05 UTC (creation time + 5months 27days 19h 12m)
+                   Invalid: The subkey is not live: Expired on 2024-12-04T22:17:48Z
+  Expiration time: 2024-12-04 22:17:48 UTC (creation time + 8years 2months 21days 3h 14m 31s)
         Key flags: transport encryption, data-at-rest encryption
            Subkey: 940237AC09C57344E2EF6213C603DD3F2C219C97
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2019-07-03T10:40:12Z
-  Expiration time: 2019-07-03 10:43:27 UTC (creation time + 2years 5months 27days 7h 41m 14s)
+  Expiration time: 2027-01-28 10:26:20 UTC (creation time + 10years 23days 12h 12m 7s)
         Key flags: transport encryption, data-at-rest encryption
            Subkey: E6F2854E8480F8B7AE4E70540A866908CFE9FFF3
-                   Revoked:
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2019-07-03T10:40:12Z
+  Expiration time: 2027-01-28 10:25:24 UTC (creation time + 10years 11months 18days 15h 5m 15s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Victor Toso (toso) <victortoso@gnome.org>
            UserID: Victor Toso <toso@posteo.net>
            UserID: Victor Toso de Carvalho (toso) <victortoso@redhat.com>
+                   Revoked:
            UserID: Victor Toso de Carvalho <me@victortoso.com>
            UserID: Victor Toso de Carvalho <vtosodec@redhat.com>
-self-signatures PositiveCertification: 2016-02-09, 2016-09-13, 2017-12-21, 2018-07-03
-self-signatures SubkeyBinding: 2016-02-09, 2016-09-13, 2018-07-03
+                   Revoked:
+self-signatures CertificationRevocation: 2026-03-15
+self-signatures PositiveCertification: 2016-02-09, 2016-09-13, 2017-12-21, 2018-07-03, 2019-07-09, 2020-08-10, 2022-08-17, 2022-12-05, 2024-12-06, 2025-01-28
+self-signatures SubkeyBinding: 2016-02-09, 2016-09-13, 2017-01-04, 2018-07-03, 2019-07-09, 2020-08-10, 2022-08-17, 2022-12-05, 2025-01-28
 self-signatures SubkeyRevocation: 2017-01-04
 third-party GenericCertification: 3
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the changed spec does not get past the signature check. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
