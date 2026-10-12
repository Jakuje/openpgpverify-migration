# Keyring refresh for nss_wrapper

**Status: proposed**

Failing call: `--keyring=/builddir/new/nss_wrapper.keyring --signature=/builddir/new/nss_wrapper-1.1.16.tar.gz.asc --data=/builddir/new/nss_wrapper-1.1.16.tar.gz`

Phase 1 reason: `sha1-cert`

## nss_wrapper.keyring

- certificates: 8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD
- size: 3432 → 18452 bytes

```diff
--- dist-git/nss_wrapper.keyring
+++ refreshed/nss_wrapper.keyring
@@ -1,17 +1,14 @@
       Fingerprint: 8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D
-                   Invalid: No binding signature at time 2026-10-12T11:56:32Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: 9D04ADDA7B3A38E6F9E74DE1668803FBFBA5A04A
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-12T11:56:32Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
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
+self-signatures PositiveCertification: 2013-10-05, 2016-03-31, 2019-07-16
 self-signatures SubkeyBinding: 2013-10-05
+third-party CasualCertification: 2
+third-party GenericCertification: 14
+third-party PositiveCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... nss_wrapper-1.1.16.tar.gz
8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D
rc=0
```

