# Keyring update from upstream for skribilo

**Status: still-fails**

Failing call: `--keyring=/builddir/new/arunisaac.pub --signature=/builddir/new/skribilo-0.11.0.tar.gz.sig --data=/builddir/new/skribilo-0.11.0.tar.gz`

Phase 1 reason: `expired`

## arunisaac.pub

- from: https://systemreboot.net/about/arunisaac.pub
- certificates (unchanged): 7F730343F2F09F3C77BF79D32E25EE8B61802BB3
- size: 4634 → 4634 bytes

```
curl -fsSL -o arunisaac.pub https://systemreboot.net/about/arunisaac.pub
```

```diff
--- dist-git/arunisaac.pub
+++ upstream/arunisaac.pub
@@ -1,10 +1,8 @@
       Fingerprint: 7F730343F2F09F3C77BF79D32E25EE8B61802BB3
-                   Invalid: The primary key is not live: Expired on 2024-03-01T09:44:40Z
-  Expiration time: 2024-03-01 09:44:40 UTC (creation time + 10years 5months 23days 1m 52s)
+  Expiration time: 2027-03-01 22:11:41 UTC (creation time + 13years 5months 22days 18h 28m 53s)
         Key flags: certification, signing
            Subkey: B7ACCF781EB7E021FD8CB1CAA6E8C999B91F5347
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2024-03-01T09:44:40Z
-  Expiration time: 2024-03-01 09:45:10 UTC (creation time + 10years 5months 23days 2m 22s)
+  Expiration time: 2027-03-01 22:13:10 UTC (creation time + 13years 5months 22days 18h 30m 22s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Arun I (My personal key) <theroarofthedragon@gmail.com>
                    Revoked:
@@ -12,6 +10,6 @@
                    because: SHA1 is not considered secure
            UserID: Arun I <arunisaac@systemreboot.net>
 self-signatures CertificationRevocation: 2016-09-23
-self-signatures PositiveCertification: 2013-09-07, 2015-10-25, 2017-03-20, 2018-03-21, 2020-03-19, 2023-03-02
-self-signatures SubkeyBinding: 2023-03-02
+self-signatures PositiveCertification: 2013-09-07, 2015-10-25, 2017-03-20, 2018-03-21, 2020-03-19, 2026-03-01
+self-signatures SubkeyBinding: 2026-03-01
 third-party GenericCertification: 1
```

## Verification with the upstream keyring

```
$ sqv ... skribilo-0.11.0.tar.gz
Signing key on 7F730343F2F09F3C77BF79D32E25EE8B61802BB3 is bad:
           The primary key is not live
  because: Expired on 2021-03-19T06:29:29Z
rc=1
```

