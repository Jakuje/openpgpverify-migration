# Keyring refresh for strongswan

**Status: still-fails**

Failing call: `--keyring=/builddir/new/STRONGSWAN-RELEASE-PGP-KEY --signature=/builddir/new/strongswan-6.1.0.tar.bz2.sig --data=/builddir/new/strongswan-6.1.0.tar.bz2`

Phase 1 reason: `sha1-cert`

## STRONGSWAN-RELEASE-PGP-KEY

- certificates: 948F158A4E76A27BF3D07532DF42C170B34DBA77
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 2915 → 18694 bytes

```diff
--- dist-git/STRONGSWAN-RELEASE-PGP-KEY
+++ refreshed/STRONGSWAN-RELEASE-PGP-KEY
@@ -9,3 +9,6 @@
                    because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2009-06-12
 self-signatures SubkeyBinding: 2009-08-20
+third-party CasualCertification: 3
+third-party GenericCertification: 22
+third-party PositiveCertification: 10
```

## Verification with the refreshed keyring

```
$ sqv ... strongswan-6.1.0.tar.bz2
Signing key on 948F158A4E76A27BF3D07532DF42C170B34DBA77 is not bound:
           No binding signature at time 2026-09-06T07:00:54Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

