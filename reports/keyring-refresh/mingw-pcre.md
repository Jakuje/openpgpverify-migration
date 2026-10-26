# Keyring refresh for mingw-pcre

**Status: proposed**

Failing call: `--keyring=/builddir/new/Public-Key --signature=/builddir/new/pcre-8.45.tar.bz2.sig --data=/builddir/new/pcre-8.45.tar.bz2`

Phase 1 reason: `sha1-cert`

## Public-Key

- certificates: 45F68D54BBE23FB3039B46E59766E084FB0F43D8
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 2201 → 24270 bytes

```diff
--- dist-git/Public-Key
+++ refreshed/Public-Key
@@ -1,14 +1,21 @@
       Fingerprint: 45F68D54BBE23FB3039B46E59766E084FB0F43D8
-                   Invalid: No binding signature at time 2026-10-26T17:50:38Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: 5B4A38D79D4DBC571BCEB95D243A73A0ECFA4A69
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-26T17:50:38Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
+           UserID: Philip Hazel <Philip.Hazel@gmail.com>
            UserID: Philip Hazel <ph10@cam.ac.uk>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
            UserID: Philip Hazel <ph10@cus.cam.ac.uk>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2002-10-21, 2002-10-23
+           UserID: Philip Hazel <ph10@hermes.cam.ac.uk>
+                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
+self-signatures PositiveCertification: 2002-10-21, 2002-10-23, 2006-03-14, 2007-05-02, 2021-03-25
 self-signatures SubkeyBinding: 2002-10-21
+third-party CasualCertification: 11
+third-party GenericCertification: 26
+third-party PositiveCertification: 13
```

## Verification with the refreshed keyring

```
$ sqv ... pcre-8.45.tar.bz2
45F68D54BBE23FB3039B46E59766E084FB0F43D8
rc=0
```

