# Keyring update from upstream for xdg-desktop-portal-wlr

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-0FDE7BE0E88F5E48.gpg --signature=/builddir/new/xdg-desktop-portal-wlr-0.8.4.tar.gz.sig --data=/builddir/new/xdg-desktop-portal-wlr-0.8.4.tar.gz`

Phase 1 reason: `expired`

## gpgkey-0FDE7BE0E88F5E48.gpg

- from: https://emersion.fr/.well-known/openpgpkey/hu/dj3498u4hyyarh35rkjfnghbjxug6b19
- certificates (unchanged): 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
- size: 2263 → 2263 bytes

```
curl -fsSL -o gpgkey-0FDE7BE0E88F5E48.gpg https://emersion.fr/.well-known/openpgpkey/hu/dj3498u4hyyarh35rkjfnghbjxug6b19
```

```diff
--- dist-git/gpgkey-0FDE7BE0E88F5E48.gpg
+++ upstream/gpgkey-0FDE7BE0E88F5E48.gpg
@@ -1,11 +1,9 @@
       Fingerprint: 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
-                   Invalid: The primary key is not live: Expired on 2021-03-04T10:03:50Z
-  Expiration time: 2021-03-04 10:03:50 UTC (creation time + 4years 11months 1day 16h 1m 56s)
+  Expiration time: 2027-04-12 16:35:43 UTC (creation time + 11years 10days 43m 25s)
         Key flags: certification, signing
            Subkey: 3842522FEB127E044BC92BEA10D018335A0B5D8E
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2021-03-04T10:03:50Z
-  Expiration time: 2021-03-04 10:05:06 UTC (creation time + 4years 11months 1day 16h 3m 12s)
+  Expiration time: 2027-04-12 16:35:24 UTC (creation time + 11years 10days 43m 6s)
         Key flags: transport encryption, data-at-rest encryption
-           UserID: emersion <contact@emersion.fr>
-self-signatures PositiveCertification: 2020-03-04
-self-signatures SubkeyBinding: 2020-03-04
+           UserID: Simon Ser <contact@emersion.fr>
+self-signatures PositiveCertification: 2026-04-12
+self-signatures SubkeyBinding: 2026-04-12
```

## Verification with the upstream keyring

```
$ sqv ... xdg-desktop-portal-wlr-0.8.4.tar.gz
34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
rc=0
```

