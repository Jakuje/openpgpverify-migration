# Keyring refresh for cswrap

**Status: proposed**

Failing call: `--keyring=/builddir/new/kdudka.pgp --signature=/builddir/new/cswrap-2.2.6.tar.xz.asc --data=/builddir/new/cswrap-2.2.6.tar.xz`

Phase 1 reason: `expired`

## kdudka.pgp

- certificates: 992A96E075056E79CD8214F9873DB37572A37B36
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 3147 → 6998 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network search --output - 992A96E075056E79CD8214F9873DB37572A37B36 \
  | sq keyring filter --experimental --cert 992A96E075056E79CD8214F9873DB37572A37B36 --output update.pgp
sq keyring merge --output kdudka.pgp.new kdudka.pgp update.pgp
mv kdudka.pgp.new kdudka.pgp
```

```diff
--- dist-git/kdudka.pgp
+++ refreshed/kdudka.pgp
@@ -1,11 +1,10 @@
       Fingerprint: 992A96E075056E79CD8214F9873DB37572A37B36
-                   Invalid: The primary key is not live: Expired on 2024-11-17T19:43:11Z
-  Expiration time: 2024-11-17 19:43:11 UTC (creation time + 8years 8days 2h 53m 37s)
+  Expiration time: 2028-11-10 14:13:46 UTC (creation time + 12years 21h 24m 12s)
         Key flags: certification, signing
            Subkey: 88042D1DA187C23513118991302A70F14BB026FE
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2024-11-17T19:43:11Z
-  Expiration time: 2024-11-17 19:43:38 UTC (creation time + 8years 8days 2h 54m 4s)
+  Expiration time: 2028-11-10 14:14:30 UTC (creation time + 12years 21h 24m 56s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Kamil Dudka <kdudka@redhat.com>
-self-signatures PositiveCertification: 2020-11-18
-self-signatures SubkeyBinding: 2020-11-18
+self-signatures PositiveCertification: 2016-11-09, 2020-11-18, 2024-11-11
+self-signatures SubkeyBinding: 2016-11-09, 2020-11-18, 2024-11-11
+third-party GenericCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... cswrap-2.2.6.tar.xz
992A96E075056E79CD8214F9873DB37572A37B36
rc=0
```

