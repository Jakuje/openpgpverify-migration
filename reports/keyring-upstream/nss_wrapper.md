# Keyring update from upstream for nss_wrapper

**Status: still-fails**

Failing call: `--keyring=/builddir/new/nss_wrapper.keyring --signature=/builddir/new/nss_wrapper-1.1.16.tar.gz.asc --data=/builddir/new/nss_wrapper-1.1.16.tar.gz`

Phase 1 reason: `sha1-cert`

## nss_wrapper.keyring

- from: https://cryptomilk.org/0x8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D_asn_cryptomilk_org_gpgkey.asc
- certificates (unchanged): 8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D
- size: 3432 → 4845 bytes

```
curl -fsSL -o nss_wrapper.keyring https://cryptomilk.org/0x8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D_asn_cryptomilk_org_gpgkey.asc
```

```diff
--- dist-git/nss_wrapper.keyring
+++ upstream/nss_wrapper.keyring
@@ -1,17 +1,9 @@
       Fingerprint: 8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D
-                   Invalid: No binding signature at time 2026-10-29T08:01:43Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: 9D04ADDA7B3A38E6F9E74DE1668803FBFBA5A04A
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-29T08:01:43Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Andreas Schneider <asn@cryptomilk.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Andreas Schneider <asn@redhat.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Andreas Schneider <asn@samba.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2013-10-05, 2016-03-31
-self-signatures SubkeyBinding: 2013-10-05
+self-signatures PositiveCertification: 2026-10-28
+self-signatures SubkeyBinding: 2026-10-28
```

## Verification with the upstream keyring

```
$ sqv ... nss_wrapper-1.1.16.tar.gz
Signing key on 8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D is not bound:
           No binding signature at time 2024-07-05T08:35:13Z
  because: No binding signature at time 2024-07-05T08:35:13Z
rc=1
```

