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
- refreshed keyring `tor-keyring.pub` (see below)
- Release bumped (`1%{?dist}` → `2%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | pass |

Tested on 2026-11-06 at dist-git commit `9d12b9ecd0c8` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (verification fails), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR replaces the keyring with the keyserver copy. No key was added or removed. Please check the fingerprint against upstream:

- `B74417EDDF22AC9F9E90F49142E86A2A11F48D36`
- `2133BC600AB133E1D826D173FE43009C4607B1FB`
- `1C1BC007A9F607AA8152C040BEA7B180B1491921`

The refresh, as run (the spec comment above the `Source` line has the same command, for the next refresh):

```
sq --home=none network keyserver search \
  B74417EDDF22AC9F9E90F49142E86A2A11F48D36 \
  2133BC600AB133E1D826D173FE43009C4607B1FB \
  1C1BC007A9F607AA8152C040BEA7B180B1491921 \
  --output tor-keyring.pub --overwrite
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/tor-keyring.pub
+++ refreshed/tor-keyring.pub
@@ -1,48 +1,11 @@
-      Fingerprint: B74417EDDF22AC9F9E90F49142E86A2A11F48D36
-                   Invalid: The primary key is not live: Expired on 2023-04-07T12:41:29Z
-  Expiration time: 2023-04-07 12:41:29 UTC (creation time + 11years 10months 26days 15h 28m 54s)
-        Key flags: certification, signing
-           Subkey: 0451E51B33B7AC38C57B09F72AC6036C93CC198D
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2023-04-07T12:41:29Z
-  Expiration time: 2023-04-07 12:42:43 UTC (creation time + 9years 6months 25days 17h 30m 30s)
-        Key flags: transport encryption, data-at-rest encryption
-           UserID: David Goulet (EfficiOS work address) <dgoulet@efficios.com>
-                   Revoked:
-                   Invalid: No binding signature at time 2026-11-06T09:25:16Z
-           UserID: David Goulet <dgoulet@ev0ke.net>
-           UserID: David Goulet <dgoulet@hackus.org>
-                   Revoked:
-                   Invalid: No binding signature at time 2026-11-06T09:25:16Z
-           UserID: David Goulet <dgoulet@riseup.net>
-           UserID: David Goulet <dgoulet@torproject.org>
-      Fingerprint: 2133BC600AB133E1D826D173FE43009C4607B1FB
-                   Invalid: The primary key is not live: Expired on 2025-10-04T13:11:01Z
-  Expiration time: 2025-10-04 13:11:01 UTC (creation time + 9years 12days 16h 16m 57s)
-        Key flags: certification
-           Subkey: 7A02B3521DC75C542BA015456AFEE6D49E92B601
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-10-04T13:11:01Z
-  Expiration time: 2025-10-04 13:12:07 UTC (creation time + 9years 10days 17h 3m 56s)
-        Key flags: signing
-           Subkey: 847EC32393A7317A3C9AF84391DDED0286AC8BFF
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-10-04T13:11:01Z
-  Expiration time: 2025-10-04 13:12:34 UTC (creation time + 9years 10days 16h 58m 20s)
-        Key flags: transport encryption, data-at-rest encryption
-           UserID: Nick Mathewson <nickm@alum.mit.edu>
-           UserID: Nick Mathewson <nickm@freehaven.net>
-           UserID: Nick Mathewson <nickm@torproject.org>
-           UserID: Nick Mathewson <nickm@wangafu.net>
       Fingerprint: 1C1BC007A9F607AA8152C040BEA7B180B1491921
-                   Invalid: The primary key is not live: Expired on 2024-12-02T19:24:13Z
-  Expiration time: 2024-12-02 19:24:13 UTC (creation time + 4years 11months 29days 3h 50m 24s)
+  Expiration time: 2029-01-20 14:13:30 UTC (creation time + 9years 1month 17days 2h 15m 41s)
         Key flags: certification, signing
            Subkey: 514102454D0A87DB0767A1EBBE6A0531C18A9179
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2024-12-02T19:24:13Z
         Key flags: signing
            Subkey: CA883563156C84476ADBF88ADE333A13667681D0
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2024-12-02T19:24:13Z
         Key flags: transport encryption, data-at-rest encryption
            Subkey: 302A9D0520D6F9B2484ABAFE135CF5D5269F803B
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2024-12-02T19:24:13Z
         Key flags: authentication
            UserID: Alexander Færøy <ahf@0x90.dk>
            UserID: Alexander Færøy <ahf@bornhack.org>
@@ -50,6 +13,42 @@
            UserID: Alexander Færøy <ahf@irc6.net>
            UserID: Alexander Færøy <ahf@irssi.org>
            UserID: Alexander Færøy <ahf@torproject.org>
+      Fingerprint: 2133BC600AB133E1D826D173FE43009C4607B1FB
+  Expiration time: 2029-06-15 14:52:31 UTC (creation time + 12years 8months 23days 11h 29m 39s)
+        Key flags: certification
+           Subkey: 7A02B3521DC75C542BA015456AFEE6D49E92B601
+  Expiration time: 2027-06-16 14:54:51 UTC (creation time + 10years 8months 22days 17m 52s)
+        Key flags: signing
+           Subkey: 847EC32393A7317A3C9AF84391DDED0286AC8BFF
+  Expiration time: 2027-06-16 14:54:43 UTC (creation time + 10years 8months 22days 11m 41s)
+        Key flags: transport encryption, data-at-rest encryption
+           UserID: Nick Mathewson <nickm@alum.mit.edu>
+           UserID: Nick Mathewson <nickm@freehaven.net>
+           UserID: Nick Mathewson <nickm@torproject.org>
+           UserID: Nick Mathewson <nickm@wangafu.net>
+      Fingerprint: B74417EDDF22AC9F9E90F49142E86A2A11F48D36
+  Expiration time: 2027-03-16 18:53:02 UTC (creation time + 15years 10months 4days 21h 40m 27s)
+        Key flags: certification, signing
+           Subkey: 0451E51B33B7AC38C57B09F72AC6036C93CC198D
+  Expiration time: 2027-03-16 18:54:05 UTC (creation time + 13years 6months 3days 23h 41m 52s)
+        Key flags: transport encryption, data-at-rest encryption
+           Subkey: 1633F1DB3D4390FEA7E88F05CD885877FE9D6620
+                   Invalid: Policy rejected asymmetric algorithm: ElGamal4096 is not considered secure
+           UserID: David Goulet (EfficiOS work address) <dgoulet@efficios.com>
+                   Revoked:
+                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
+           UserID: David Goulet <dgoulet@ev0ke.net>
+           UserID: David Goulet <dgoulet@hackus.org>
+                   Revoked:
+                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
+           UserID: David Goulet <dgoulet@riseup.net>
+           UserID: David Goulet <dgoulet@torproject.org>
 self-signatures CertificationRevocation: 2013-09-25, 2015-05-14
-self-signatures PositiveCertification: 2019-12-04, 2019-12-05, 2020-10-05, 2022-04-07
-self-signatures SubkeyBinding: 2019-12-04, 2020-10-05, 2022-04-07
+self-signatures GenericCertification: 2016-10-04
+self-signatures PositiveCertification: 2011-05-11, 2011-12-12, 2013-08-18, 2014-02-23, 2016-05-09, 2016-09-21, 2016-09-23, 2016-10-09, 2017-05-01, 2018-05-01, 2018-09-17, 2019-05-01, 2019-12-04, 2019-12-05, 2020-04-30, 2020-10-05, 2021-04-08, 2022-04-07, 2023-04-09, 2025-01-21, 2025-03-24, 2026-03-16, 2026-06-16
+self-signatures SubkeyBinding: 2011-05-11, 2013-09-10, 2014-09-10, 2015-09-11, 2016-08-20, 2016-09-23, 2017-08-07, 2018-08-17, 2018-09-17, 2019-08-17, 2019-08-19, 2019-12-04, 2020-04-30, 2020-10-05, 2021-04-08, 2022-04-07, 2023-04-09, 2025-03-24, 2026-03-16, 2026-06-16
+third-party CasualCertification: 11
+third-party GenericCertification: 79
+third-party PositiveCertification: 16
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is dropped too. To check that nothing else needs it, the changed spec was built completely (`rpmbuild -bb`; the spec has no `%check`) in a chroot with gnupg2 and gpgverify removed, and the build log doesn't mention gpg.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
