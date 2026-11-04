# Keyring update from upstream for cage

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-E88F5E48.gpg --signature=/builddir/new/cage-0.3.1.tar.gz.sig --data=/builddir/new/cage-0.3.1.tar.gz`

Phase 1 reason: `expired`

## gpgkey-E88F5E48.gpg

- from: https://keys.openpgp.org/vks/v1/by-fingerprint/34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48#/gpgkey-0FDE7BE0E88F5E48.asc
- **renamed to `gpgkey-0FDE7BE0E88F5E48.asc`; its `Source` line becomes the URL**
- certificates (unchanged): 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
- size: 16093 → 22487 bytes

```
curl -fsSL -o gpgkey-0FDE7BE0E88F5E48.asc 'https://keys.openpgp.org/vks/v1/by-fingerprint/34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48'
```

```diff
--- dist-git/gpgkey-E88F5E48.gpg
+++ upstream/gpgkey-E88F5E48.gpg
@@ -1,12 +1,10 @@
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
```

## Verification with the upstream keyring

```
$ sqv ... cage-0.3.1.tar.gz
34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
rc=0
```

