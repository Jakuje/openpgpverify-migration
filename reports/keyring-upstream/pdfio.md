# Keyring update from upstream for pdfio

**Status: proposed**

Failing call: `--keyring=/builddir/new/msweet-pub.gpg --signature=/builddir/new/pdfio-1.6.5.tar.gz.sig --data=/builddir/new/pdfio-1.6.5.tar.gz`

Phase 1 reason: `expired`

## msweet-pub.gpg

- from: https://keys.openpgp.org/vks/v1/by-fingerprint/9086C3CDC66C3F563CF8F405BE67C75EC81F3244#/msweet-pub.asc
- **renamed to `msweet-pub.asc`; its `Source` line becomes the URL**
- certificates (unchanged): 9086C3CDC66C3F563CF8F405BE67C75EC81F3244
- size: 3151 → 5657 bytes

```
curl -fsSL -o msweet-pub.asc 'https://keys.openpgp.org/vks/v1/by-fingerprint/9086C3CDC66C3F563CF8F405BE67C75EC81F3244'
```

```diff
--- dist-git/msweet-pub.gpg
+++ upstream/msweet-pub.gpg
@@ -1,11 +1,10 @@
       Fingerprint: 9086C3CDC66C3F563CF8F405BE67C75EC81F3244
-                   Invalid: The primary key is not live: Expired on 2024-10-30T22:06:43Z
-  Expiration time: 2024-10-30 22:06:43 UTC (creation time + 4years)
+  Expiration time: 2029-11-01 19:05:45 UTC (creation time + 9years 1day 14h 59m 2s)
         Key flags: certification, signing
            Subkey: C53DB51FF598C6F84B524FBEA692FD1B4D815AE0
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2024-10-30T22:06:43Z
-  Expiration time: 2024-10-30 22:06:43 UTC (creation time + 4years)
+                   Invalid: The subkey is not live: Expired on 2026-11-01T20:05:46Z
+  Expiration time: 2026-11-01 20:05:46 UTC (creation time + 6years 1day 9h 59m 3s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Michael R Sweet <msweet@msweet.org>
-self-signatures PositiveCertification: 2020-10-30
-self-signatures SubkeyBinding: 2020-10-30
+self-signatures PositiveCertification: 2020-10-30, 2024-11-01, 2025-11-11
+self-signatures SubkeyBinding: 2020-10-30, 2024-11-01
```

## Verification with the upstream keyring

```
$ sqv ... pdfio-1.6.5.tar.gz
9086C3CDC66C3F563CF8F405BE67C75EC81F3244
rc=0
```

