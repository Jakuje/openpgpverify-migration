# Keyring refresh for bemenu

**Status: proposed**

Failing call: `--keyring=/builddir/new/bemenu-pgp.txt --signature=/builddir/new/bemenu-0.6.23.tar.gz.asc --data=/builddir/new/bemenu-0.6.23.tar.gz`

Phase 1 reason: `expired`

## bemenu-pgp.txt

- certificates: 16B6B7CACAF339DECE9F154729317348D687B86B
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 2850 → 4077 bytes

```diff
--- dist-git/bemenu-pgp.txt
+++ refreshed/bemenu-pgp.txt
@@ -1,12 +1,8 @@
       Fingerprint: 16B6B7CACAF339DECE9F154729317348D687B86B
-                   Invalid: The primary key is not live: Expired on 2023-05-20T00:57:03Z
-  Expiration time: 2023-05-20 00:57:03 UTC (creation time + 1year 11months 29days 21h 50m 24s)
         Key flags: certification, signing
            Subkey: 553B84F554B6A81DCB701BB3662C8D5062CC4609
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2023-05-20T00:57:03Z
-  Expiration time: 2023-05-20 00:57:03 UTC (creation time + 1year 11months 29days 21h 50m 24s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Bemenu Upstream
-self-signatures PositiveCertification: 2021-05-20
-self-signatures SubkeyBinding: 2021-05-20
+self-signatures PositiveCertification: 2021-05-20, 2023-08-29
+self-signatures SubkeyBinding: 2021-05-20, 2023-08-29
 third-party GenericCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... bemenu-0.6.23.tar.gz
16B6B7CACAF339DECE9F154729317348D687B86B
rc=0
```

