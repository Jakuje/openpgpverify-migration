# Keyring update from upstream for skribilo

**Status: proposed**

Failing call: `--keyring=/builddir/new/arunisaac.pub --signature=/builddir/new/skribilo-0.11.0.tar.gz.sig --data=/builddir/new/skribilo-0.11.0.tar.gz`

Phase 1 reason: `expired`

## arunisaac.pub

- from: https://keys.openpgp.org/vks/v1/by-fingerprint/7F730343F2F09F3C77BF79D32E25EE8B61802BB3#/arunisaac.pub
- certificates (unchanged): 7F730343F2F09F3C77BF79D32E25EE8B61802BB3
- size: 4634 → 3719 bytes

```
curl -fsSL -o arunisaac.pub 'https://keys.openpgp.org/vks/v1/by-fingerprint/7F730343F2F09F3C77BF79D32E25EE8B61802BB3'
```

```diff
--- dist-git/arunisaac.pub
+++ upstream/arunisaac.pub
@@ -1,17 +1,11 @@
       Fingerprint: 7F730343F2F09F3C77BF79D32E25EE8B61802BB3
-                   Invalid: The primary key is not live: Expired on 2024-03-01T09:44:40Z
-  Expiration time: 2024-03-01 09:44:40 UTC (creation time + 10years 5months 23days 1m 52s)
+                   Invalid: The primary key is not live: Expired on 2026-03-01T19:09:07Z
+  Expiration time: 2026-03-01 19:09:07 UTC (creation time + 12years 5months 22days 21h 26m 19s)
         Key flags: certification, signing
            Subkey: B7ACCF781EB7E021FD8CB1CAA6E8C999B91F5347
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2024-03-01T09:44:40Z
-  Expiration time: 2024-03-01 09:45:10 UTC (creation time + 10years 5months 23days 2m 22s)
+                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-03-01T19:09:07Z
+  Expiration time: 2026-03-01 19:09:57 UTC (creation time + 12years 5months 22days 21h 27m 9s)
         Key flags: transport encryption, data-at-rest encryption
-           UserID: Arun I (My personal key) <theroarofthedragon@gmail.com>
-                   Revoked:
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Arun I <arunisaac@systemreboot.net>
-self-signatures CertificationRevocation: 2016-09-23
-self-signatures PositiveCertification: 2013-09-07, 2015-10-25, 2017-03-20, 2018-03-21, 2020-03-19, 2023-03-02
-self-signatures SubkeyBinding: 2023-03-02
-third-party GenericCertification: 1
+self-signatures PositiveCertification: 2015-10-25, 2017-03-20, 2018-03-21, 2020-03-19, 2025-03-01
+self-signatures SubkeyBinding: 2025-03-01
```

## Verification with the upstream keyring

```
$ sqv ... skribilo-0.11.0.tar.gz
7F730343F2F09F3C77BF79D32E25EE8B61802BB3
rc=0
```

