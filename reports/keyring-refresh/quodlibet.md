# Keyring refresh for quodlibet

**Status: proposed**

Failing call: `--keyring=/builddir/new/E0AA0F031DBD80FFBA57B06D5A62D0CAB6264964 --signature=/builddir/new/quodlibet-4.7.1.tar.gz.sig --data=/builddir/new/quodlibet-4.7.1.tar.gz`

Phase 1 reason: `expired`

## E0AA0F031DBD80FFBA57B06D5A62D0CAB6264964

- certificates: 0EBF782C5D53F7E5FB02A66746BD761F7A49B0EC
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 33442 → 49219 bytes

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

## Verification with the refreshed keyring

```
$ sqv ... quodlibet-4.7.1.tar.gz
0EBF782C5D53F7E5FB02A66746BD761F7A49B0EC
rc=0
```

