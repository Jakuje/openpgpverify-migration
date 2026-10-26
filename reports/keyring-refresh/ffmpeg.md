# Keyring refresh for ffmpeg

**Status: still-fails**

Failing call: `--keyring=/builddir/new/ffmpeg.keyring --signature=/builddir/new/ffmpeg-9.0.2.tar.xz.asc --data=/builddir/new/ffmpeg-9.0.2.tar.xz`

Phase 1 reason: `sha1-cert`

## ffmpeg.keyring

- certificates: FCF986EA15E6E293A5644F10B4322F04D67658D8
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 1203 → 6527 bytes

```diff
--- dist-git/ffmpeg.keyring
+++ refreshed/ffmpeg.keyring
@@ -9,3 +9,7 @@
                    because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2011-04-26
 self-signatures SubkeyBinding: 2011-04-26
+third-party CasualCertification: 1
+third-party CertificationRevocation: 1
+third-party GenericCertification: 15
+third-party PositiveCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... ffmpeg-9.0.2.tar.xz
Signing key on FCF986EA15E6E293A5644F10B4322F04D67658D8 is not bound:
           No binding signature at time 2026-09-18T02:46:02Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

