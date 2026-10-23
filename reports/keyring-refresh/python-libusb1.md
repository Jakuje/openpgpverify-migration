# Keyring refresh for python-libusb1

**Status: still-fails**

Failing call: `--keyring=/builddir/new/gpgkey-python-libusb1.gpg --signature=/builddir/new/libusb1-3.4.0.tar.gz.asc --data=/builddir/new/libusb1-3.4.0.tar.gz`

Phase 1 reason: `sha1-cert`

## gpgkey-python-libusb1.gpg

- certificates: 983AE8B73B9115987A923845CAC936914257B0C1
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 7034 → 7871 bytes

```diff
--- dist-git/gpgkey-python-libusb1.gpg
+++ refreshed/gpgkey-python-libusb1.gpg
@@ -8,7 +8,8 @@
                    Invalid: primary key: No binding signature at time 2026-10-23T08:15:07Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
            UserID: Vincent Pelletier <pelletier.vincent@wanadoo.fr>
                    Revoked:
-                   Invalid: No binding signature at time 2026-10-23T08:15:07Z
+                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
            UserID: Vincent Pelletier <plr.vincent@gmail.com>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
```

## Verification with the refreshed keyring

```
$ sqv ... libusb1-3.4.0.tar.gz
Signing key on 983AE8B73B9115987A923845CAC936914257B0C1 is not bound:
           No binding signature at time 2026-05-16T20:57:41Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

