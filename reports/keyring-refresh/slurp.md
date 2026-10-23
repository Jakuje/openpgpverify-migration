# Keyring refresh for slurp

**Status: proposed**

Failing call: `--keyring=/builddir/new/dj3498u4hyyarh35rkjfnghbjxug6b19 --signature=/builddir/new/slurp-1.5.0.tar.gz.sig --data=/builddir/new/slurp-1.5.0.tar.gz`

Phase 1 reason: `sha1-cert`

## dj3498u4hyyarh35rkjfnghbjxug6b19

- certificates: 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 2263 → 17527 bytes

```diff
--- dist-git/dj3498u4hyyarh35rkjfnghbjxug6b19
+++ refreshed/dj3498u4hyyarh35rkjfnghbjxug6b19
@@ -1,11 +1,12 @@
       Fingerprint: 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
-                   Invalid: No binding signature at time 2026-10-23T08:15:16Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2027-04-12 16:35:43 UTC (creation time + 11years 10days 43m 25s)
+        Key flags: certification, signing
            Subkey: 3842522FEB127E044BC92BEA10D018335A0B5D8E
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-23T08:15:16Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
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
+third-party CasualCertification: 1
+third-party GenericCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... slurp-1.5.0.tar.gz
34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
rc=0
```

