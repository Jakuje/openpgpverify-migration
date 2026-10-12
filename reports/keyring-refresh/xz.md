# Keyring refresh for xz

**Status: proposed**

Failing call: `--keyring=/builddir/new/lasse_collin_pubkey.txt --signature=/builddir/new/xz-5.8.4.tar.gz.sig --data=/builddir/new/xz-5.8.4.tar.gz`

Phase 1 reason: `expired`

## lasse_collin_pubkey.txt

- certificates: 3690C240CE51B4670D30AD1C38EE757D69184620
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keyserver.ubuntu.com
- size: 3151 → 21603 bytes

```diff
--- dist-git/lasse_collin_pubkey.txt
+++ refreshed/lasse_collin_pubkey.txt
@@ -1,11 +1,10 @@
       Fingerprint: 3690C240CE51B4670D30AD1C38EE757D69184620
-                   Invalid: The primary key is not live: Expired on 2025-02-07T14:42:17Z
-  Expiration time: 2025-02-07 14:42:17 UTC (creation time + 14years 3months 15days 5h 11m 19s)
+  Expiration time: 2027-02-10 10:00:01 UTC (creation time + 16years 3months 17days 12h 29m 3s)
         Key flags: certification, signing
            Subkey: 06D04A6B37AF445DABE0D6DA5923A9D358ADF744
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-02-07T14:42:17Z
-  Expiration time: 2025-02-07 14:41:54 UTC (creation time + 14years 3months 15days 5h 10m 56s)
+  Expiration time: 2027-02-10 10:00:06 UTC (creation time + 16years 3months 17days 12h 29m 8s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Lasse Collin <lasse.collin@tukaani.org>
-self-signatures PositiveCertification: 2024-01-08
-self-signatures SubkeyBinding: 2024-01-08
+self-signatures PositiveCertification: 2010-10-24, 2015-01-24, 2016-09-10, 2019-01-20, 2020-03-16, 2021-03-12, 2022-09-30, 2024-01-08, 2025-01-08, 2026-01-16
+self-signatures SubkeyBinding: 2010-10-24, 2015-01-24, 2016-09-10, 2019-01-20, 2020-03-16, 2021-03-12, 2022-09-30, 2024-01-08, 2025-01-08, 2026-01-16
+third-party GenericCertification: 6
```

## Verification with the refreshed keyring

```
$ sqv ... xz-5.8.4.tar.gz
3690C240CE51B4670D30AD1C38EE757D69184620
rc=0
```

