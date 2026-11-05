# Keyring update from upstream for samba

**Status: proposed**

Failing call: `--keyring=/builddir/new/samba-pubkey_AA99442FB680B620.gpg --signature=/builddir/new/samba-4.25.1.tar.asc --data=-`

Phase 1 reason: `expired`

## samba-pubkey_AA99442FB680B620.gpg

- from: https://download.samba.org/pub/samba/samba-pubkey.asc
- **renamed to `samba-pubkey.asc`; its `Source` line becomes the URL**
- **adds keys the URL also holds: 9147A339719518EE9011BCB54793916113084025** (asked for)
- certificates (unchanged): 81F5E2832BD2545A1897B713AA99442FB680B620
- size: 2290 → 10638 bytes

```
curl -fsSL -O https://download.samba.org/pub/samba/samba-pubkey.asc
```

```diff
--- dist-git/samba-pubkey_AA99442FB680B620.gpg
+++ upstream/samba-pubkey_AA99442FB680B620.gpg
@@ -1,11 +1,18 @@
       Fingerprint: 81F5E2832BD2545A1897B713AA99442FB680B620
-                   Invalid: The primary key is not live: Expired on 2022-12-21T12:11:00Z
-  Expiration time: 2022-12-21 12:11:00 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2027-12-12 17:06:40 UTC (creation time + 6years 11months 20days 20h 46m 4s)
         Key flags: certification, signing
            Subkey: 8ECB3E1AD3C66464249027DE97EF9386FBFD4002
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-12-21T12:11:00Z
-  Expiration time: 2022-12-21 12:11:00 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2027-12-12 17:09:32 UTC (creation time + 6years 11months 20days 20h 48m 56s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Samba Distribution Verification Key <samba-bugs@samba.org>
-self-signatures PositiveCertification: 2020-12-21
-self-signatures SubkeyBinding: 2020-12-21
+      Fingerprint: 9147A339719518EE9011BCB54793916113084025
+  Expiration time: 2027-12-13 12:18:24 UTC (creation time + 16years 10months 30days 6h 51m 33s)
+        Key flags: certification, signing
+           Subkey: 541FB94987D491A3C201D8B1B1DD08BF65F64DAB
+  Expiration time: 2027-12-13 12:18:38 UTC (creation time + 16years 10months 30days 6h 51m 47s)
+        Key flags: transport encryption, data-at-rest encryption
+           UserID: Samba Library Distribution Key <samba-bugs@samba.org>
+self-signatures PositiveCertification: 2011-01-12, 2012-01-21, 2013-01-27, 2014-03-20, 2015-04-29, 2016-05-06, 2017-06-02, 2018-06-26, 2019-07-03, 2020-07-09, 2020-12-21, 2022-12-19, 2023-12-18, 2024-10-15, 2025-12-12, 2025-12-13
+self-signatures SubkeyBinding: 2025-12-12, 2025-12-13
+third-party GenericCertification: 3
+third-party PositiveCertification: 1
```

Host verification skipped (data from stdin or a generated file); run phase1.py after approval.

