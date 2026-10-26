# Keyring refresh for unrealircd

**Status: still-fails**

Failing call: `--keyring=/builddir/new/gpgkey-1D2D2B03A0B68ED11D68A24BA7A21B0A108FF4A9.gpg --signature=/builddir/new/unrealircd-6.1.10.tar.gz.asc --data=/builddir/new/unrealircd-6.1.10.tar.gz`

Phase 1 reason: `sha1-cert`

## gpgkey-1D2D2B03A0B68ED11D68A24BA7A21B0A108FF4A9.gpg

- certificates: 1D2D2B03A0B68ED11D68A24BA7A21B0A108FF4A9
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, WKD; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 1199 → 3352 bytes

```diff
--- dist-git/gpgkey-1D2D2B03A0B68ED11D68A24BA7A21B0A108FF4A9.gpg
+++ refreshed/gpgkey-1D2D2B03A0B68ED11D68A24BA7A21B0A108FF4A9.gpg
@@ -4,3 +4,5 @@
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2015-07-02
+third-party CasualCertification: 1
+third-party GenericCertification: 4
```

## Verification with the refreshed keyring

```
$ sqv ... unrealircd-6.1.10.tar.gz
Signing key on 1D2D2B03A0B68ED11D68A24BA7A21B0A108FF4A9 is not bound:
           No binding signature at time 2025-03-07T13:59:02Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

