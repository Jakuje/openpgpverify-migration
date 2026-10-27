# Keyring update from upstream for wlroots

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-0FDE7BE0E88F5E48.gpg --signature=/builddir/new/wlroots-0.20.2.tar.gz.sig --data=/builddir/new/wlroots-0.20.2.tar.gz`

Phase 1 reason: `expired`

## gpgkey-0FDE7BE0E88F5E48.gpg

- from: https://emersion.fr/.well-known/openpgpkey/hu/dj3498u4hyyarh35rkjfnghbjxug6b19
- certificates (unchanged): 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
- size: 8249 → 2263 bytes

```
curl -fsSL -o gpgkey-0FDE7BE0E88F5E48.gpg https://emersion.fr/.well-known/openpgpkey/hu/dj3498u4hyyarh35rkjfnghbjxug6b19
```

```diff
--- dist-git/gpgkey-0FDE7BE0E88F5E48.gpg
+++ upstream/gpgkey-0FDE7BE0E88F5E48.gpg
@@ -1,13 +1,9 @@
       Fingerprint: 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
-                   Invalid: The primary key is not live: Expired on 2022-03-10T17:55:59Z
-  Expiration time: 2022-03-10 17:55:59 UTC (creation time + 5years 11months 7days 17h 54m 5s)
+  Expiration time: 2027-04-12 16:35:43 UTC (creation time + 11years 10days 43m 25s)
         Key flags: certification, signing
            Subkey: 3842522FEB127E044BC92BEA10D018335A0B5D8E
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-03-10T17:55:59Z
-  Expiration time: 2022-03-10 17:56:33 UTC (creation time + 5years 11months 7days 17h 54m 39s)
+  Expiration time: 2027-04-12 16:35:24 UTC (creation time + 11years 10days 43m 6s)
         Key flags: transport encryption, data-at-rest encryption
-           UserID: emersion <contact@emersion.fr>
-self-signatures PositiveCertification: 2016-04-01, 2017-04-01, 2018-04-02, 2019-03-11, 2019-04-08, 2021-03-10
-self-signatures SubkeyBinding: 2019-04-08, 2021-03-10
-third-party CasualCertification: 1
-third-party GenericCertification: 1
+           UserID: Simon Ser <contact@emersion.fr>
+self-signatures PositiveCertification: 2026-04-12
+self-signatures SubkeyBinding: 2026-04-12
```

## Verification with the upstream keyring

```
$ sqv ... wlroots-0.20.2.tar.gz
34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
rc=0
```

