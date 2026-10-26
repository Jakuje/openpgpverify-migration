# Keyring refresh for znc

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-5AE420CC0209989E.asc --signature=/builddir/new/znc-1.10.3.tar.gz.sig --data=/builddir/new/znc-1.10.3.tar.gz`

Phase 1 reason: `sha1-cert`

## gpgkey-5AE420CC0209989E.asc

- certificates: D5823CACB477191CAC0075555AE420CC0209989E
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 5576 → 31840 bytes

```diff
--- dist-git/gpgkey-5AE420CC0209989E.asc
+++ refreshed/gpgkey-5AE420CC0209989E.asc
@@ -1,21 +1,19 @@
       Fingerprint: D5823CACB477191CAC0075555AE420CC0209989E
-                   Invalid: No binding signature at time 2026-10-26T20:14:28Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2030-02-17 23:55:54 UTC (creation time + 18years 3months 9days 12h 24m 10s)
+        Key flags: certification, signing
            Subkey: A1951C9AE193C618F082AE7F17611B1A40BDEDED
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-26T20:14:28Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2030-02-17 23:55:36 UTC (creation time + 18years 3months 9days 12h 23m 52s)
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Alexey Sokolov (ZNC) <alexey+znc@asokolov.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
+           UserID: Alexey Sokolov <alexey+gentoo@asokolov.org>
            UserID: Alexey Sokolov <alexey@alexeysokolov.co.cc>
                    Revoked:
-                   Invalid: No binding signature at time 2026-10-26T20:14:28Z
-           UserID: Alexey Sokolov <alexey@asokolov.org>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
+           UserID: Alexey Sokolov <alexey@asokolov.org>
            UserID: Alexey Sokolov <ktonibud@gmail.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
+           UserID: Alexey Sokolov <sokolov@google.com>
 self-signatures CertificationRevocation: 2015-12-09
-self-signatures PositiveCertification: 2017-01-08
-self-signatures SubkeyBinding: 2017-01-08
+self-signatures PositiveCertification: 2011-11-09, 2013-06-09, 2013-11-04, 2016-08-27, 2017-01-08, 2019-12-23, 2020-05-24, 2022-12-25, 2025-02-18
+self-signatures SubkeyBinding: 2011-11-09, 2013-06-09, 2016-08-27, 2017-01-08, 2019-12-23, 2022-12-25, 2025-02-18
+third-party GenericCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... znc-1.10.3.tar.gz
D5823CACB477191CAC0075555AE420CC0209989E
rc=0
```

