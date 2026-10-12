# Keyring refresh for libtpms

**Status: still-fails**

Failing call: `--keyring=/builddir/new/gpgkey-B818B9CADF9089C2D5CEC66B75AD65802A0B4211.asc --signature=/builddir/new/libtpms-0.10.2.tar.gz.asc --data=/builddir/new/libtpms-0.10.2.tar.gz`

Phase 1 reason: `sha1-cert`

## gpgkey-B818B9CADF9089C2D5CEC66B75AD65802A0B4211.asc

- certificates: B818B9CADF9089C2D5CEC66B75AD65802A0B4211
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 945 → 1680 bytes

```diff
--- dist-git/gpgkey-B818B9CADF9089C2D5CEC66B75AD65802A0B4211.asc
+++ refreshed/gpgkey-B818B9CADF9089C2D5CEC66B75AD65802A0B4211.asc
@@ -1,6 +1,7 @@
       Fingerprint: B818B9CADF9089C2D5CEC66B75AD65802A0B4211
-                   Invalid: No binding signature at time 2026-10-12T11:55:42Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: No binding signature at time 2026-10-12T11:55:43Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
            UserID: Stefan Berger <stefanb@linux.vnet.ibm.com>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2017-10-04
+third-party GenericCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... libtpms-0.10.2.tar.gz
Signing key on B818B9CADF9089C2D5CEC66B75AD65802A0B4211 is not bound:
           No binding signature at time 2026-01-02T16:06:58Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

