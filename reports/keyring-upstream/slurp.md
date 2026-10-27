# Keyring update from upstream for slurp

**Status: still-fails**

Failing call: `--keyring=/builddir/new/dj3498u4hyyarh35rkjfnghbjxug6b19 --signature=/builddir/new/slurp-1.5.0.tar.gz.sig --data=/builddir/new/slurp-1.5.0.tar.gz`

Phase 1 reason: `sha1-cert`

## dj3498u4hyyarh35rkjfnghbjxug6b19

- from: https://emersion.fr/.well-known/openpgpkey/hu/dj3498u4hyyarh35rkjfnghbjxug6b19
- certificates (unchanged): 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
- size: 2263 → 2263 bytes

```
curl -fsSL -o dj3498u4hyyarh35rkjfnghbjxug6b19 https://emersion.fr/.well-known/openpgpkey/hu/dj3498u4hyyarh35rkjfnghbjxug6b19
```

```diff
--- dist-git/dj3498u4hyyarh35rkjfnghbjxug6b19
+++ upstream/dj3498u4hyyarh35rkjfnghbjxug6b19
@@ -1,11 +1,9 @@
       Fingerprint: 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
-                   Invalid: No binding signature at time 2026-10-27T11:31:42Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2027-04-12 16:35:43 UTC (creation time + 11years 10days 43m 25s)
+        Key flags: certification, signing
            Subkey: 3842522FEB127E044BC92BEA10D018335A0B5D8E
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-27T11:31:42Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: emersion <contact@emersion.fr>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2019-04-08
-self-signatures SubkeyBinding: 2019-04-08
+  Expiration time: 2027-04-12 16:35:24 UTC (creation time + 11years 10days 43m 6s)
+        Key flags: transport encryption, data-at-rest encryption
+           UserID: Simon Ser <contact@emersion.fr>
+self-signatures PositiveCertification: 2026-04-12
+self-signatures SubkeyBinding: 2026-04-12
```

## Verification with the upstream keyring

```
$ sqv ... slurp-1.5.0.tar.gz
Signing key on 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48 is not bound:
           No binding signature at time 2023-12-14T10:56:21Z
  because: No binding signature at time 2023-12-14T10:56:21Z
rc=1
```

