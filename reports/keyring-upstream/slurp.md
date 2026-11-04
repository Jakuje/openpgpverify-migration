# Keyring update from upstream for slurp

**Status: proposed**

Failing call: `--keyring=/builddir/new/dj3498u4hyyarh35rkjfnghbjxug6b19 --signature=/builddir/new/slurp-1.5.0.tar.gz.sig --data=/builddir/new/slurp-1.5.0.tar.gz`

Phase 1 reason: `sha1-cert`

## dj3498u4hyyarh35rkjfnghbjxug6b19

- from: https://keys.openpgp.org/vks/v1/by-fingerprint/34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48#/gpgkey-0FDE7BE0E88F5E48.asc
- **renamed to `gpgkey-0FDE7BE0E88F5E48.asc`; its `Source` line becomes the URL**
- certificates (unchanged): 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
- size: 2263 → 22487 bytes

```
curl -fsSL -o gpgkey-0FDE7BE0E88F5E48.asc 'https://keys.openpgp.org/vks/v1/by-fingerprint/34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48'
```

```diff
--- dist-git/dj3498u4hyyarh35rkjfnghbjxug6b19
+++ upstream/dj3498u4hyyarh35rkjfnghbjxug6b19
@@ -1,11 +1,10 @@
       Fingerprint: 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
-                   Invalid: No binding signature at time 2026-11-04T16:12:35Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2027-04-12 16:35:43 UTC (creation time + 11years 10days 43m 25s)
+        Key flags: certification, signing
            Subkey: 3842522FEB127E044BC92BEA10D018335A0B5D8E
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-04T16:12:35Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2027-04-12 16:35:24 UTC (creation time + 11years 10days 43m 6s)
+        Key flags: transport encryption, data-at-rest encryption
+           UserID: Simon Ser <contact@emersion.fr>
            UserID: emersion <contact@emersion.fr>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2019-04-08
-self-signatures SubkeyBinding: 2019-04-08
+self-signatures PositiveCertification: 2016-04-01, 2017-04-01, 2018-04-02, 2019-03-11, 2019-04-08, 2020-03-04, 2021-03-10, 2022-03-30, 2023-04-01, 2023-04-21, 2024-04-03, 2025-04-12, 2026-04-12
+self-signatures SubkeyBinding: 2016-04-01, 2017-04-01, 2018-04-02, 2019-04-08, 2020-03-04, 2021-03-10, 2022-03-30, 2023-04-01, 2024-04-03, 2025-04-12, 2026-04-12
```

## Verification with the upstream keyring

```
$ sqv ... slurp-1.5.0.tar.gz
34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
rc=0
```

