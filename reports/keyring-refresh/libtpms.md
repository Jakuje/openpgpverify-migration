# Keyring refresh for libtpms

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-B818B9CADF9089C2D5CEC66B75AD65802A0B4211.asc --signature=/builddir/new/libtpms-0.10.2.tar.gz.asc --data=/builddir/new/libtpms-0.10.2.tar.gz`

Phase 1 reason: `sha1-cert`

## gpgkey-B818B9CADF9089C2D5CEC66B75AD65802A0B4211.asc

- certificates: B818B9CADF9089C2D5CEC66B75AD65802A0B4211
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 945 → 2810 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network keyserver search B818B9CADF9089C2D5CEC66B75AD65802A0B4211 --output gpgkey-B818B9CADF9089C2D5CEC66B75AD65802A0B4211.asc --overwrite
```

```diff
--- dist-git/gpgkey-B818B9CADF9089C2D5CEC66B75AD65802A0B4211.asc
+++ refreshed/gpgkey-B818B9CADF9089C2D5CEC66B75AD65802A0B4211.asc
@@ -1,6 +1,7 @@
       Fingerprint: B818B9CADF9089C2D5CEC66B75AD65802A0B4211
-                   Invalid: No binding signature at time 2026-11-11T10:28:53Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2027-10-02 15:51:34 UTC (creation time + 9years 11months 27days 21h 50m 24s)
+        Key flags: certification, signing
+           UserID: Stefan Berger <stefanb@linux.ibm.com>
            UserID: Stefan Berger <stefanb@linux.vnet.ibm.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2017-10-04
+self-signatures PositiveCertification: 2017-10-04, 2026-11-10
+third-party GenericCertification: 1
```

## libtpms-0.10.2.tar.gz.asc (new release signature)

- from: https://github.com/stefanberger/libtpms/releases/download/v0.10.2/v0.10.2.tar.gz.asc
- size: 525 → 525 bytes
- SHA512, made 2026-11-10 19:42:57, by `B818B9CADF9089C2D5CEC66B75AD65802A0B4211`

## Verification with the refreshed keyring

```
$ sqv ... libtpms-0.10.2.tar.gz
B818B9CADF9089C2D5CEC66B75AD65802A0B4211
rc=0
```

