# Keyring refresh for wlroots0.19

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-0FDE7BE0E88F5E48.gpg --signature=/builddir/new/wlroots-0.19.3.tar.gz.sig --data=/builddir/new/wlroots-0.19.3.tar.gz`

Phase 1 reason: `expired`

## gpgkey-0FDE7BE0E88F5E48.gpg

- certificates: 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 8249 → 18875 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network search --output - 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48 \
  | sq keyring filter --experimental --cert 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48 --output update.pgp
sq keyring merge gpgkey-0FDE7BE0E88F5E48.gpg update.pgp | sq packet dearmor --output gpgkey-0FDE7BE0E88F5E48.gpg.new
mv gpgkey-0FDE7BE0E88F5E48.gpg.new gpgkey-0FDE7BE0E88F5E48.gpg
```

```diff
--- dist-git/gpgkey-0FDE7BE0E88F5E48.gpg
+++ refreshed/gpgkey-0FDE7BE0E88F5E48.gpg
@@ -1,13 +1,12 @@
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
+           UserID: Simon Ser <contact@emersion.fr>
            UserID: emersion <contact@emersion.fr>
-self-signatures PositiveCertification: 2016-04-01, 2017-04-01, 2018-04-02, 2019-03-11, 2019-04-08, 2021-03-10
-self-signatures SubkeyBinding: 2019-04-08, 2021-03-10
+self-signatures PositiveCertification: 2016-04-01, 2017-04-01, 2018-04-02, 2019-03-11, 2019-04-08, 2020-03-04, 2021-03-10, 2022-03-30, 2023-04-01, 2023-04-21, 2024-04-03, 2025-04-12, 2026-04-12
+self-signatures SubkeyBinding: 2016-04-01, 2017-04-01, 2018-04-02, 2019-04-08, 2020-03-04, 2021-03-10, 2022-03-30, 2023-04-01, 2024-04-03, 2025-04-12, 2026-04-12
 third-party CasualCertification: 1
 third-party GenericCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... wlroots-0.19.3.tar.gz
34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
rc=0
```

