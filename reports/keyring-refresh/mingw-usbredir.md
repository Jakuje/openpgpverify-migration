# Keyring refresh for mingw-usbredir

**Status: proposed**

Failing call: `--keyring=/builddir/new/victortoso-E37A484F.keyring --signature=/builddir/new/usbredir-0.14.0.tar.xz.sig --data=/builddir/new/usbredir-0.14.0.tar.xz`

Phase 1 reason: `expired`

## victortoso-E37A484F.keyring

- certificates: 206D3B352F566F3B0E6572E997D9123DE37A484F
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 19943 → 46814 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network search --output - 206D3B352F566F3B0E6572E997D9123DE37A484F \
  | sq keyring filter --experimental --cert 206D3B352F566F3B0E6572E997D9123DE37A484F --output update.pgp
sq keyring merge victortoso-E37A484F.keyring update.pgp | sq packet dearmor --output victortoso-E37A484F.keyring.new
mv victortoso-E37A484F.keyring.new victortoso-E37A484F.keyring
```

```diff
--- dist-git/victortoso-E37A484F.keyring
+++ refreshed/victortoso-E37A484F.keyring
@@ -1,26 +1,25 @@
       Fingerprint: 206D3B352F566F3B0E6572E997D9123DE37A484F
-                   Invalid: The primary key is not live: Expired on 2019-07-03T10:40:12Z
-  Expiration time: 2019-07-03 10:40:12 UTC (creation time + 3years 4months 22days 11h 15m 15s)
+  Expiration time: 2027-01-28 10:25:47 UTC (creation time + 10years 11months 18days 15h 5m 38s)
         Key flags: certification, signing
            Subkey: 64EE94DD16CF2DECEBCFA62BE98F5B4819679A78
-                   Revoked:
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2019-07-03T10:40:12Z
-  Expiration time: 2017-03-12 21:56:05 UTC (creation time + 5months 27days 19h 12m)
+                   Invalid: The subkey is not live: Expired on 2024-12-04T22:17:48Z
+  Expiration time: 2024-12-04 22:17:48 UTC (creation time + 8years 2months 21days 3h 14m 31s)
         Key flags: transport encryption, data-at-rest encryption
            Subkey: 940237AC09C57344E2EF6213C603DD3F2C219C97
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2019-07-03T10:40:12Z
-  Expiration time: 2019-07-03 10:43:27 UTC (creation time + 2years 5months 27days 7h 41m 14s)
+  Expiration time: 2027-01-28 10:26:20 UTC (creation time + 10years 23days 12h 12m 7s)
         Key flags: transport encryption, data-at-rest encryption
            Subkey: E6F2854E8480F8B7AE4E70540A866908CFE9FFF3
-                   Revoked:
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2019-07-03T10:40:12Z
+  Expiration time: 2027-01-28 10:25:24 UTC (creation time + 10years 11months 18days 15h 5m 15s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Victor Toso (toso) <victortoso@gnome.org>
            UserID: Victor Toso <toso@posteo.net>
            UserID: Victor Toso de Carvalho (toso) <victortoso@redhat.com>
+                   Revoked:
            UserID: Victor Toso de Carvalho <me@victortoso.com>
            UserID: Victor Toso de Carvalho <vtosodec@redhat.com>
-self-signatures PositiveCertification: 2016-02-09, 2016-09-13, 2017-12-21, 2018-07-03
-self-signatures SubkeyBinding: 2016-02-09, 2016-09-13, 2018-07-03
+                   Revoked:
+self-signatures CertificationRevocation: 2026-03-15
+self-signatures PositiveCertification: 2016-02-09, 2016-09-13, 2017-12-21, 2018-07-03, 2019-07-09, 2020-08-10, 2022-08-17, 2022-12-05, 2024-12-06, 2025-01-28
+self-signatures SubkeyBinding: 2016-02-09, 2016-09-13, 2017-01-04, 2018-07-03, 2019-07-09, 2020-08-10, 2022-08-17, 2022-12-05, 2025-01-28
 self-signatures SubkeyRevocation: 2017-01-04
 third-party GenericCertification: 3
```

## Verification with the refreshed keyring

```
$ sqv ... usbredir-0.14.0.tar.xz
206D3B352F566F3B0E6572E997D9123DE37A484F
rc=0
```

