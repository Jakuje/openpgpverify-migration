# Keyring update from upstream for ffmpeg

**Status: still-fails**

Failing call: `--keyring=/builddir/new/ffmpeg.keyring --signature=/builddir/new/ffmpeg-9.0.2.tar.xz.asc --data=/builddir/new/ffmpeg-9.0.2.tar.xz`

Phase 1 reason: `sha1-cert`

## ffmpeg.keyring

- from: https://ffmpeg.org/ffmpeg-devel.asc
- certificates (unchanged): FCF986EA15E6E293A5644F10B4322F04D67658D8
- size: 1203 → 1709 bytes

```
curl -fsSL -o ffmpeg.keyring https://ffmpeg.org/ffmpeg-devel.asc
```

```diff
(no change in sq inspect summary)
```

## Verification with the upstream keyring

```
$ sqv ... ffmpeg-9.0.2.tar.xz
Signing key on FCF986EA15E6E293A5644F10B4322F04D67658D8 is not bound:
           No binding signature at time 2026-09-18T02:46:02Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

