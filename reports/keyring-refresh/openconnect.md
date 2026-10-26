# Keyring refresh for openconnect

**Status: still-fails**

Failing call: `--keyring=/builddir/new/gpgkey-BE07D9FD54809AB2C4B0FF5F63762CDA67E2F359.asc --signature=/builddir/new/openconnect-9.21.tar.gz.asc --data=/builddir/new/openconnect-9.21.tar.gz`

Phase 1 reason: `sha1-cert`

## gpgkey-BE07D9FD54809AB2C4B0FF5F63762CDA67E2F359.asc

- certificates: BE07D9FD54809AB2C4B0FF5F63762CDA67E2F359
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD
- size: 11026 → 271414 bytes
- **warning: refreshed keyring is 271414 bytes (flooded third-party signatures?)**

```diff
--- dist-git/gpgkey-BE07D9FD54809AB2C4B0FF5F63762CDA67E2F359.asc
+++ refreshed/gpgkey-BE07D9FD54809AB2C4B0FF5F63762CDA67E2F359.asc
@@ -16,23 +16,8 @@
            UserID: David Woodhouse <dwmw2@kernel.org>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-      Fingerprint: BE07D9FD54809AB2C4B0FF5F63762CDA67E2F359
-                   Invalid: No binding signature at time 2026-10-26T17:51:41Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: FEBC6502361A4AB69B1E8FB99E4D3FFB166DFD78
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-26T17:51:41Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: David Woodhouse <david@woodhou.se>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: David Woodhouse <dwmw2@exim.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: David Woodhouse <dwmw2@infradead.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: David Woodhouse <dwmw2@kernel.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2011-10-06, 2011-10-07, 2011-11-25
 self-signatures SubkeyBinding: 2011-10-06
+third-party CasualCertification: 1
+third-party GenericCertification: 40
+third-party PositiveCertification: 4
```

## Verification with the refreshed keyring

```
$ sqv ... openconnect-9.21.tar.gz
Signing key on BE07D9FD54809AB2C4B0FF5F63762CDA67E2F359 is not bound:
           No binding signature at time 2026-06-16T11:33:09Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

