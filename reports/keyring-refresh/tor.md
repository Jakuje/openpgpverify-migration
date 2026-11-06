# Keyring refresh for tor

**Status: proposed**

Failing call: `--keyring=/builddir/new/tor-keyring.pub --signature=/builddir/new/tor-0.4.9.15.tar.gz.sha256sum.asc --data=/builddir/new/tor-0.4.9.15.tar.gz.sha256sum`

Phase 1 reason: `concatenated-armor`

## tor-keyring.pub

- certificates: B74417EDDF22AC9F9E90F49142E86A2A11F48D36, 2133BC600AB133E1D826D173FE43009C4607B1FB, 1C1BC007A9F607AA8152C040BEA7B180B1491921
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 14237 → 313529 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network keyserver search \
  B74417EDDF22AC9F9E90F49142E86A2A11F48D36 \
  2133BC600AB133E1D826D173FE43009C4607B1FB \
  1C1BC007A9F607AA8152C040BEA7B180B1491921 \
  --output tor-keyring.pub --overwrite
```
- **warning: refreshed keyring is 313529 bytes (flooded third-party signatures?)**

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

## Verification with the refreshed keyring

```
$ sqv ... tor-0.4.9.15.tar.gz.sha256sum
B74417EDDF22AC9F9E90F49142E86A2A11F48D36
rc=0
```

