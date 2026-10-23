# Keyring refresh for drm_info

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-0FDE7BE0E88F5E48.gpg --signature=/builddir/new/drm_info-2.10.0.tar.gz.sig --data=/builddir/new/drm_info-2.10.0.tar.gz`

Phase 1 reason: `expired`

## gpgkey-0FDE7BE0E88F5E48.gpg

- certificates: 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 7501 → 17527 bytes

```diff
--- dist-git/gpgkey-0FDE7BE0E88F5E48.gpg
+++ refreshed/gpgkey-0FDE7BE0E88F5E48.gpg
@@ -1,13 +1,12 @@
       Fingerprint: 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
-                   Invalid: The primary key is not live: Expired on 2023-03-30T09:26:17Z
-  Expiration time: 2023-03-30 09:26:17 UTC (creation time + 6years 11months 27days 3h 24m 23s)
+  Expiration time: 2027-04-12 16:35:43 UTC (creation time + 11years 10days 43m 25s)
         Key flags: certification, signing
            Subkey: 3842522FEB127E044BC92BEA10D018335A0B5D8E
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2023-03-30T09:26:17Z
-  Expiration time: 2023-03-30 09:26:39 UTC (creation time + 6years 11months 27days 3h 24m 45s)
+  Expiration time: 2027-04-12 16:35:24 UTC (creation time + 11years 10days 43m 6s)
         Key flags: transport encryption, data-at-rest encryption
+           UserID: Simon Ser <contact@emersion.fr>
            UserID: emersion <contact@emersion.fr>
-self-signatures PositiveCertification: 2016-04-01, 2017-04-01, 2018-04-02, 2019-03-11, 2019-04-08, 2020-03-04, 2022-03-30
-self-signatures SubkeyBinding: 2020-03-04, 2022-03-30
+self-signatures PositiveCertification: 2016-04-01, 2017-04-01, 2018-04-02, 2019-03-11, 2019-04-08, 2020-03-04, 2021-03-10, 2022-03-30, 2023-04-01, 2023-04-21, 2024-04-03, 2025-04-12, 2026-04-12
+self-signatures SubkeyBinding: 2016-04-01, 2017-04-01, 2018-04-02, 2019-04-08, 2020-03-04, 2021-03-10, 2022-03-30, 2023-04-01, 2024-04-03, 2025-04-12, 2026-04-12
 third-party CasualCertification: 1
 third-party GenericCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... drm_info-2.10.0.tar.gz
34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
rc=0
```

