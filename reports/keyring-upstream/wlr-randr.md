# Keyring update from upstream for wlr-randr

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-0FDE7BE0E88F5E48.gpg --signature=/builddir/new/wlr-randr-0.5.0.tar.gz.sig --data=/builddir/new/wlr-randr-0.5.0.tar.gz`

Phase 1 reason: `expired`

## gpgkey-0FDE7BE0E88F5E48.gpg

- from: https://keys.openpgp.org/vks/v1/by-fingerprint/34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48#/gpgkey-0FDE7BE0E88F5E48.asc
- **renamed to `gpgkey-0FDE7BE0E88F5E48.asc`; its `Source` line becomes the URL**
- certificates (unchanged): 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
- size: 7501 → 22487 bytes

```
curl -fsSL -o gpgkey-0FDE7BE0E88F5E48.asc 'https://keys.openpgp.org/vks/v1/by-fingerprint/34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48'
```

```diff
--- dist-git/gpgkey-0FDE7BE0E88F5E48.gpg
+++ upstream/gpgkey-0FDE7BE0E88F5E48.gpg
@@ -1,13 +1,10 @@
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
-third-party CasualCertification: 1
-third-party GenericCertification: 1
+self-signatures PositiveCertification: 2016-04-01, 2017-04-01, 2018-04-02, 2019-03-11, 2019-04-08, 2020-03-04, 2021-03-10, 2022-03-30, 2023-04-01, 2023-04-21, 2024-04-03, 2025-04-12, 2026-04-12
+self-signatures SubkeyBinding: 2016-04-01, 2017-04-01, 2018-04-02, 2019-04-08, 2020-03-04, 2021-03-10, 2022-03-30, 2023-04-01, 2024-04-03, 2025-04-12, 2026-04-12
```

## Verification with the upstream keyring

```
$ sqv ... wlr-randr-0.5.0.tar.gz
34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
rc=0
```

