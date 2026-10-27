# Keyring update from upstream for libdvdnav

**Status: still-fails**

Failing call: `--keyring=/builddir/new/7180713BE58D1ADC.asc --signature=/builddir/new/libdvdnav-7.0.0.tar.xz.asc --data=/builddir/new/libdvdnav-7.0.0.tar.xz`

Phase 1 reason: `sha1-sig`

## 7180713BE58D1ADC.asc

- from: https://download.videolan.org/pub/keys/7180713BE58D1ADC.asc
- certificates (unchanged): 65F7C6B4206BD057A7EB73787180713BE58D1ADC
- size: 7177 → 17142 bytes

```
curl -fsSL -o 7180713BE58D1ADC.asc https://download.videolan.org/pub/keys/7180713BE58D1ADC.asc
```

```diff
--- dist-git/7180713BE58D1ADC.asc
+++ upstream/7180713BE58D1ADC.asc
@@ -12,5 +12,11 @@
            UserID: VideoLAN Release Signing Key (2016)
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2013-01-21, 2014-02-02, 2015-02-11, 2016-02-18, 2016-04-26, 2017-05-03
-third-party GenericCertification: 9
+           UserID: VideoLAN Release Signing Key (2017)
+                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
+           UserID: VideoLAN Release Signing Key (2018)
+                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
+self-signatures PositiveCertification: 2013-01-21, 2014-02-02, 2015-02-11, 2016-02-18, 2016-04-26, 2017-05-03, 2017-06-07, 2026-09-14
+third-party GenericCertification: 13
```

## Verification with the upstream keyring

```
$ sqv ... libdvdnav-7.0.0.tar.xz
Signing key on 65F7C6B4206BD057A7EB73787180713BE58D1ADC is not bound:
           No binding signature at time 2025-09-30T20:22:15Z
  because: No binding signature at time 2025-09-30T20:22:15Z
rc=1
```

