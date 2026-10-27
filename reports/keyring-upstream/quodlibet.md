# Keyring update from upstream for quodlibet

**Status: proposed**

Failing call: `--keyring=/builddir/new/E0AA0F031DBD80FFBA57B06D5A62D0CAB6264964 --signature=/builddir/new/quodlibet-4.7.1.tar.gz.sig --data=/builddir/new/quodlibet-4.7.1.tar.gz`

Phase 1 reason: `expired`

## E0AA0F031DBD80FFBA57B06D5A62D0CAB6264964

- from: https://keys.openpgp.org/vks/v1/by-fingerprint/E0AA0F031DBD80FFBA57B06D5A62D0CAB6264964
- certificates (unchanged): 0EBF782C5D53F7E5FB02A66746BD761F7A49B0EC
- size: 33442 → 39979 bytes

```
curl -fsSL -o E0AA0F031DBD80FFBA57B06D5A62D0CAB6264964 https://keys.openpgp.org/vks/v1/by-fingerprint/E0AA0F031DBD80FFBA57B06D5A62D0CAB6264964
```

```diff
--- dist-git/E0AA0F031DBD80FFBA57B06D5A62D0CAB6264964
+++ upstream/E0AA0F031DBD80FFBA57B06D5A62D0CAB6264964
@@ -1,15 +1,13 @@
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
+third-party CertificationRevocation: 2
```

## Verification with the upstream keyring

```
$ sqv ... quodlibet-4.7.1.tar.gz
0EBF782C5D53F7E5FB02A66746BD761F7A49B0EC
rc=0
```

