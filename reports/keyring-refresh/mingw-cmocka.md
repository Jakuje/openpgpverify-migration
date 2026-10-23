# Keyring refresh for mingw-cmocka

**Status: proposed**

Failing call: `--keyring=/builddir/new/cmocka.keyring --signature=/builddir/new/cmocka-1.1.8.tar.xz.asc --data=/builddir/new/cmocka-1.1.8.tar.xz`

Phase 1 reason: `sha1-cert`

## cmocka.keyring

- certificates: 8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD
- size: 3432 → 18452 bytes

```diff
--- dist-git/cmocka.keyring
+++ refreshed/cmocka.keyring
@@ -1,17 +1,14 @@
       Fingerprint: 8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D
-                   Invalid: No binding signature at time 2026-10-23T08:14:45Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: 9D04ADDA7B3A38E6F9E74DE1668803FBFBA5A04A
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-23T08:14:45Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
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
$ sqv ... cmocka-1.1.8.tar.xz
8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D
rc=0
```

