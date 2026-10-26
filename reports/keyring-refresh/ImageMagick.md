# Keyring refresh for ImageMagick

**Status: still-fails**

Failing call: `--keyring=/builddir/new/ImageMagick.keyring --signature=/builddir/new/ImageMagick-7.1.2-34.tar.xz.asc --data=/builddir/new/ImageMagick-7.1.2-34.tar.xz`

Phase 1 reason: `sha1-cert`

## ImageMagick.keyring

- certificates: D8272EF51DA223E4D05B466989AB63D48277377A
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 3174 → 5483 bytes

```diff
--- dist-git/ImageMagick.keyring
+++ refreshed/ImageMagick.keyring
@@ -9,3 +9,4 @@
                    because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2013-07-01
 self-signatures SubkeyBinding: 2013-07-01
+third-party GenericCertification: 4
```

## Verification with the refreshed keyring

```
$ sqv ... ImageMagick-7.1.2-34.tar.xz
Signing key on D8272EF51DA223E4D05B466989AB63D48277377A is not bound:
           No binding signature at time 2026-10-15T01:19:41Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

