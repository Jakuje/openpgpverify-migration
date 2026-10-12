# Keyring refresh for pcsc-lite

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-F5E11B9FFE911146F41D953D78A1B4DFE8F9C57E.gpg --signature=/builddir/new/pcsc-lite-2.5.2.tar.xz.asc --data=/builddir/new/pcsc-lite-2.5.2.tar.xz`

Phase 1 reason: `sha1-cert`

## gpgkey-F5E11B9FFE911146F41D953D78A1B4DFE8F9C57E.gpg

- certificates: F5E11B9FFE911146F41D953D78A1B4DFE8F9C57E
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 14174 → 24687 bytes

```diff
--- dist-git/gpgkey-F5E11B9FFE911146F41D953D78A1B4DFE8F9C57E.gpg
+++ refreshed/gpgkey-F5E11B9FFE911146F41D953D78A1B4DFE8F9C57E.gpg
@@ -1,18 +1,19 @@
       Fingerprint: F5E11B9FFE911146F41D953D78A1B4DFE8F9C57E
-                   Invalid: No binding signature at time 2026-10-12T11:56:53Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: 1FB866BC68EFCC584B1A974B2533629C5982E499
-                   Invalid: primary key: No binding signature at time 2026-10-12T11:56:53Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: The subkey is not live: Expired on 2012-12-03T16:19:52Z
+  Expiration time: 2012-12-03 16:19:52 UTC (creation time + 11months 30days 3h 50m 24s)
+        Key flags: signing
            Subkey: AF1912CE1D685FF5ACF7C26E36A241532F1BEFF0
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-12T11:56:53Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: transport encryption, data-at-rest encryption
+           Subkey: 2C7657A42E6C6465E14CD591A782179B0F37B7F7
+                   Invalid: The subkey is not live: Expired on 2016-02-19T14:14:14Z
+  Expiration time: 2016-02-19 14:14:14 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Ludovic Rousseau <ludovic.rousseau@free.fr>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Ludovic Rousseau <rousseau@debian.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2010-09-19
-self-signatures SubkeyBinding: 2010-09-19, 2011-12-04
-third-party GenericCertification: 4
+self-signatures PositiveCertification: 2010-09-19, 2025-03-20
+self-signatures SubkeyBinding: 2010-09-19, 2011-12-04, 2014-02-19, 2025-03-20
+third-party CasualCertification: 2
+third-party GenericCertification: 8
 third-party PositiveCertification: 3
```

## Verification with the refreshed keyring

```
$ sqv ... pcsc-lite-2.5.2.tar.xz
F5E11B9FFE911146F41D953D78A1B4DFE8F9C57E
rc=0
```

