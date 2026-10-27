# Keyring update from upstream for nginx-mod-fancyindex

**Status: still-fails**

Failing call: `--keyring=/builddir/new/5AA3BC334FD7E3369E7C77B291C559DBE4C9123B --signature=/builddir/new/ngx-fancyindex-0.6.0.tar.xz.sig --data=/builddir/new/ngx-fancyindex-0.6.0.tar.xz`

Phase 1 reason: `weak-key`

## 5AA3BC334FD7E3369E7C77B291C559DBE4C9123B

- from: https://keys.openpgp.org/vks/v1/by-fingerprint/5AA3BC334FD7E3369E7C77B291C559DBE4C9123B
- certificates (unchanged): 5AA3BC334FD7E3369E7C77B291C559DBE4C9123B
- size: 4434 → 5628 bytes

```
curl -fsSL -o 5AA3BC334FD7E3369E7C77B291C559DBE4C9123B https://keys.openpgp.org/vks/v1/by-fingerprint/5AA3BC334FD7E3369E7C77B291C559DBE4C9123B
```

```diff
--- dist-git/5AA3BC334FD7E3369E7C77B291C559DBE4C9123B
+++ upstream/5AA3BC334FD7E3369E7C77B291C559DBE4C9123B
@@ -1,10 +1,8 @@
       Fingerprint: 5AA3BC334FD7E3369E7C77B291C559DBE4C9123B
                    Invalid: Policy rejected asymmetric algorithm: DSA1024 is not considered secure
            Subkey: 86578FD638E90525130ADF4976D146E5CE5D1038
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
                    Invalid: primary key: Policy rejected asymmetric algorithm, because DSA1024 is not considered secure
            UserID: Adrián Pérez de Castro (personal) <adrian@perezdecastro.org>
            UserID: Adrián Pérez de Castro <aperez@igalia.com>
-self-signatures PositiveCertification: 2008-06-02, 2015-07-16, 2016-05-11, 2018-05-12, 2020-05-12, 2022-05-11
-self-signatures SubkeyBinding: 2008-06-02
+self-signatures PositiveCertification: 2008-06-02, 2015-07-16, 2016-05-11, 2018-05-12, 2020-05-12, 2022-05-11, 2024-04-14, 2026-03-16
+self-signatures SubkeyBinding: 2008-06-02, 2026-03-16
```

## Verification with the upstream keyring

```
$ sqv ... ngx-fancyindex-0.6.0.tar.xz
Signing key on 5AA3BC334FD7E3369E7C77B291C559DBE4C9123B is not bound:
           Policy rejected asymmetric algorithm
  because: DSA1024 is not considered secure
rc=1
```

