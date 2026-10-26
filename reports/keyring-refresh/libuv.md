# Keyring refresh for libuv

**Status: proposed**

Failing call: `--keyring=/builddir/new/keysuv.gpg --signature=/builddir/new/libuv-v1.52.1.tar.gz.sign --data=/builddir/new/libuv-v1.52.1.tar.gz`

Phase 1 reason: `expired`

## keysuv.gpg

- certificates: 612F0EAD9401622379DF4402F28C3C8DA33C03BE, C82FA3AE1CBEDC6BE46B9360C43CEC45C17AB93C, CFBB9CA9A5BEAFD70E2B3C5A79A67C55A3679C8B, AEAD0A4B686767751A0E4AEF34A25FB128246514, 57353E0DBDAAA7E839B66A1AFF47D5E4AD8B4FDC, 94AE36675C464D64BAFA68DD7434390BDBE9B9C5, FDF519364458319FA8233DC9410E5553AE9BC059, D77B1E34243FBAF05F8E9CC34F55C8C846AB89B9
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 23079 → 42607 bytes

```diff
--- dist-git/keysuv.gpg
+++ refreshed/keysuv.gpg
@@ -1,19 +1,17 @@
       Fingerprint: 612F0EAD9401622379DF4402F28C3C8DA33C03BE
-                   Invalid: The primary key is not live: Expired on 2025-06-28T22:21:50Z
-  Expiration time: 2025-06-28 22:21:50 UTC (creation time + 8years 10months 2days 4h 52m 2s)
+  Expiration time: 2030-06-29 16:54:38 UTC (creation time + 13years 10months 2days 17h 24m 50s)
         Key flags: certification, signing
            Subkey: 789091C99345138DF82158EF9221D4B6ABB7F18A
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-06-28T22:21:50Z
-  Expiration time: 2025-06-28 22:22:00 UTC (creation time + 8years 10months 2days 4h 52m 12s)
+  Expiration time: 2030-06-29 16:53:19 UTC (creation time + 13years 10months 2days 17h 23m 31s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Santiago Gimeno (sgimeno) <santiago.gimeno@gmail.com>
       Fingerprint: C82FA3AE1CBEDC6BE46B9360C43CEC45C17AB93C
-                   Invalid: No binding signature at time 2026-10-26T20:11:41Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: C4960C6DAA2AEBC352F3E5B8E140F61BC5979DCC
-                   Invalid: primary key: No binding signature at time 2026-10-26T20:11:41Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: transport encryption, data-at-rest encryption
+           UserID: Richard Lau <richard.lau@ibm.com>
            UserID: Richard Lau <riclau@uk.ibm.com>
                    Revoked:
-                   Invalid: No binding signature at time 2026-10-26T20:11:41Z
            UserID: Richard Lau <rlau@redhat.com>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
@@ -69,5 +67,10 @@
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
 self-signatures CertificationRevocation: 2021-06-22
-self-signatures PositiveCertification: 2012-07-24, 2013-06-12, 2015-07-21, 2018-10-26, 2020-09-25, 2020-10-01, 2021-07-07, 2022-03-05, 2023-06-29
-self-signatures SubkeyBinding: 2012-07-24, 2013-06-12, 2015-07-21, 2018-11-01, 2019-10-28, 2020-09-25, 2021-07-07, 2022-03-05, 2023-06-29
+self-signatures GenericCertification: 2022-03-05
+self-signatures PositiveCertification: 2012-07-24, 2013-06-12, 2015-07-21, 2016-08-26, 2018-10-26, 2019-10-28, 2020-02-07, 2020-09-25, 2020-10-01, 2021-07-07, 2022-03-05, 2023-06-29, 2025-06-25, 2025-06-30
+self-signatures SubkeyBinding: 2012-07-24, 2013-06-12, 2015-07-21, 2016-08-26, 2018-11-01, 2019-10-28, 2020-02-07, 2020-09-25, 2021-07-07, 2022-03-05, 2023-06-29, 2025-06-30
+third-party CasualCertification: 2
+third-party GenericCertification: 18
+third-party PersonaCertification: 1
+third-party PositiveCertification: 4
```

## Verification with the refreshed keyring

```
$ sqv ... libuv-v1.52.1.tar.gz
612F0EAD9401622379DF4402F28C3C8DA33C03BE
rc=0
```

