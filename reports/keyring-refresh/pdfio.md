# Keyring refresh for pdfio

**Status: proposed**

Failing call: `--keyring=/builddir/new/msweet-pub.gpg --signature=/builddir/new/pdfio-1.6.5.tar.gz.sig --data=/builddir/new/pdfio-1.6.5.tar.gz`

Phase 1 reason: `expired`

## msweet-pub.gpg

- certificates: 9086C3CDC66C3F563CF8F405BE67C75EC81F3244
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 3151 → 5552 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network search --output - 9086C3CDC66C3F563CF8F405BE67C75EC81F3244 \
  | sq keyring filter --experimental --cert 9086C3CDC66C3F563CF8F405BE67C75EC81F3244 --output update.pgp
sq keyring merge --output msweet-pub.gpg.new msweet-pub.gpg update.pgp
mv msweet-pub.gpg.new msweet-pub.gpg
```

```diff
--- dist-git/msweet-pub.gpg
+++ refreshed/msweet-pub.gpg
@@ -1,11 +1,9 @@
       Fingerprint: 9086C3CDC66C3F563CF8F405BE67C75EC81F3244
-                   Invalid: The primary key is not live: Expired on 2024-10-30T22:06:43Z
-  Expiration time: 2024-10-30 22:06:43 UTC (creation time + 4years)
+  Expiration time: 2029-11-01 19:05:45 UTC (creation time + 9years 1day 14h 59m 2s)
         Key flags: certification, signing
            Subkey: C53DB51FF598C6F84B524FBEA692FD1B4D815AE0
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2024-10-30T22:06:43Z
-  Expiration time: 2024-10-30 22:06:43 UTC (creation time + 4years)
+  Expiration time: 2026-11-01 20:05:46 UTC (creation time + 6years 1day 9h 59m 3s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Michael R Sweet <msweet@msweet.org>
-self-signatures PositiveCertification: 2020-10-30
-self-signatures SubkeyBinding: 2020-10-30
+self-signatures PositiveCertification: 2020-10-30, 2024-11-01, 2025-11-11
+self-signatures SubkeyBinding: 2020-10-30, 2024-11-01
```

## Verification with the refreshed keyring

```
$ sqv ... pdfio-1.6.5.tar.gz
9086C3CDC66C3F563CF8F405BE67C75EC81F3244
rc=0
```

