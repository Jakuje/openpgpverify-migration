# Keyring refresh for isync

**Status: still-fails**

Failing call: `--keyring=/builddir/new/isync.keyring --signature=/builddir/new/isync-1.5.1.tar.gz.asc --data=/builddir/new/isync-1.5.1.tar.gz`

Phase 1 reason: `expired`

## isync.keyring

- certificates: 63BFD037CAD71E8DFF3AEA3AC17714F08D1BDBBA
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 16174 → 20120 bytes

```diff
--- dist-git/isync.keyring
+++ refreshed/isync.keyring
@@ -1,17 +1,14 @@
       Fingerprint: 63BFD037CAD71E8DFF3AEA3AC17714F08D1BDBBA
-                   Invalid: The primary key is not live: Expired on 2022-05-22T16:31:18Z
-  Expiration time: 2022-05-22 16:31:18 UTC (creation time + 3years 29days 9h 14m 51s)
+  Expiration time: 2026-11-27 17:33:49 UTC (creation time + 7years 7months 5days 8h 22m 10s)
         Key flags: certification, signing
            Subkey: 106457B8735659A4D40F56456F5447F95D001D85
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-05-22T16:31:18Z
-  Expiration time: 2022-05-22 16:34:02 UTC (creation time + 3years 29days 9h 13m 26s)
+  Expiration time: 2026-11-27 17:34:20 UTC (creation time + 7years 7months 5days 8h 18m 32s)
         Key flags: signing
            Subkey: 1193FAC0741B1EEAB7C14FDA811085B0F8931DC5
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-05-22T16:31:18Z
-  Expiration time: 2022-05-22 16:34:02 UTC (creation time + 3years 29days 9h 12m 21s)
+  Expiration time: 2026-11-27 17:34:20 UTC (creation time + 7years 7months 5days 8h 17m 27s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Oswald Buddenhagen <ossi@kde.org>
            UserID: Oswald Buddenhagen <oswald.buddenhagen@gmx.de>
-self-signatures PositiveCertification: 2019-04-23, 2020-05-06, 2021-05-22
-self-signatures SubkeyBinding: 2019-04-23, 2020-05-06, 2021-05-22
+self-signatures PositiveCertification: 2019-04-23, 2020-05-06, 2021-05-22, 2025-11-27
+self-signatures SubkeyBinding: 2019-04-23, 2020-05-06, 2021-05-22, 2025-11-27
 third-party GenericCertification: 2
```

## Verification with the refreshed keyring

```
$ sqv ... isync-1.5.1.tar.gz
Signing key on 63BFD037CAD71E8DFF3AEA3AC17714F08D1BDBBA is bad:
           The primary key is not live
  because: Expired on 2022-05-22T16:31:18Z
rc=1
```

