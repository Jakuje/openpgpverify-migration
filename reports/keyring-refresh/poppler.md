# Keyring refresh for poppler

**Status: proposed**

Failing call: `--keyring=/builddir/new/armored-keys.asc --signature=/builddir/new/poppler-26.08.0.tar.xz.sig --data=/builddir/new/poppler-26.08.0.tar.xz`

Phase 1 reason: `expired`

## armored-keys.asc

- certificates: CA262C6C83DE4D2FB28A332A3A6A4DB839EAA6D7
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 26912 → 28338 bytes

```diff
--- dist-git/armored-keys.asc
+++ refreshed/armored-keys.asc
@@ -1,13 +1,12 @@
       Fingerprint: CA262C6C83DE4D2FB28A332A3A6A4DB839EAA6D7
-                   Invalid: The primary key is not live: Expired on 2023-08-19T21:59:58Z
-  Expiration time: 2023-08-19 21:59:58 UTC (creation time + 6years 11months 13days 1h 24m 48s)
+  Expiration time: 2027-09-07 21:20:59 UTC (creation time + 11years 1day 14h 55m 25s)
         Key flags: certification, signing
            Subkey: 8692A42FB1A8B666C51053919D17D97FD8224750
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2023-08-19T21:59:58Z
-  Expiration time: 2021-08-13 21:31:53 UTC (creation time + 4years 11months 7days 12h 56m 43s)
+  Expiration time: 2027-09-07 10:00:03 UTC (creation time + 11years 1day 3h 34m 29s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Albert Astals Cid <aacid@kde.org>
-self-signatures PositiveCertification: 2016-09-05, 2018-05-16, 2018-07-31, 2019-08-14, 2020-07-28, 2021-08-01, 2022-08-18
-self-signatures SubkeyBinding: 2016-09-05, 2018-07-31, 2019-08-14, 2020-07-28
+self-signatures PositiveCertification: 2016-09-05, 2018-05-16, 2018-07-31, 2019-08-14, 2020-07-28, 2021-08-01, 2022-08-18, 2023-09-07, 2026-04-20
+self-signatures SubkeyBinding: 2016-09-05, 2018-07-31, 2019-08-14, 2020-07-28, 2024-12-12, 2026-04-20
+third-party CasualCertification: 1
 third-party GenericCertification: 13
 third-party PositiveCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... poppler-26.08.0.tar.xz
CA262C6C83DE4D2FB28A332A3A6A4DB839EAA6D7
rc=0
```

