# Keyring refresh for kdsoap

**Status: still-fails**

Failing call: `--keyring=/builddir/new/kdab-products.asc --signature=/builddir/new/kdsoap-2.2.0.tar.gz.asc --data=/builddir/new/kdsoap-2.2.0.tar.gz`

Phase 1 reason: `sha1-cert`

## kdab-products.asc

- certificates: E86C000370B1B9E2A9191AD53DBFB6882C9358FB
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 1644 → 2094 bytes

```diff
--- dist-git/kdab-products.asc
+++ refreshed/kdab-products.asc
@@ -4,3 +4,4 @@
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2017-05-01
+third-party GenericCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... kdsoap-2.2.0.tar.gz
Signing key on E86C000370B1B9E2A9191AD53DBFB6882C9358FB is not bound:
           No binding signature at time 2024-01-07T16:47:49Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

