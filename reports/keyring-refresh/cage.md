# Keyring refresh for cage

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-E88F5E48.gpg --signature=/builddir/new/cage-0.3.1.tar.gz.sig --data=/builddir/new/cage-0.3.1.tar.gz`

Phase 1 reason: `expired`

## gpgkey-E88F5E48.gpg

- certificates: 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://mail-api.proton.me
- size: 16093 → 23817 bytes

```diff
--- dist-git/gpgkey-E88F5E48.gpg
+++ refreshed/gpgkey-E88F5E48.gpg
@@ -1,12 +1,12 @@
       Fingerprint: 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
-                   Invalid: The primary key is not live: Expired on 2024-03-31T12:47:54Z
-  Expiration time: 2024-03-31 12:47:54 UTC (creation time + 7years 11months 29days 46m)
+  Expiration time: 2027-04-12 16:35:43 UTC (creation time + 11years 10days 43m 25s)
         Key flags: certification, signing
            Subkey: 3842522FEB127E044BC92BEA10D018335A0B5D8E
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2024-03-31T12:47:54Z
-  Expiration time: 2024-03-31 12:48:08 UTC (creation time + 7years 11months 29days 46m 14s)
+  Expiration time: 2027-04-12 16:35:24 UTC (creation time + 11years 10days 43m 6s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Simon Ser <contact@emersion.fr>
            UserID: emersion <contact@emersion.fr>
-self-signatures PositiveCertification: 2016-04-01, 2017-04-01, 2018-04-02, 2019-03-11, 2019-04-08, 2020-03-04, 2021-03-10, 2022-03-30, 2023-04-01
-self-signatures SubkeyBinding: 2016-04-01, 2017-04-01, 2018-04-02, 2019-04-08, 2020-03-04, 2021-03-10, 2022-03-30, 2023-04-01
+self-signatures PositiveCertification: 2016-04-01, 2017-04-01, 2018-04-02, 2019-03-11, 2019-04-08, 2020-03-04, 2021-03-10, 2022-03-30, 2023-04-01, 2023-04-21, 2024-04-03, 2025-04-12, 2026-04-12
+self-signatures SubkeyBinding: 2016-04-01, 2017-04-01, 2018-04-02, 2019-04-08, 2020-03-04, 2021-03-10, 2022-03-30, 2023-04-01, 2024-04-03, 2025-04-12, 2026-04-12
+third-party CasualCertification: 1
+third-party GenericCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... cage-0.3.1.tar.gz
34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
rc=0
```

