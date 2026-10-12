# Keyring refresh for libidn2

**Status: proposed**

Failing call: `--keyring=/builddir/new/B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE --signature=/builddir/new/libidn2-2.3.8.tar.gz.sig --data=/builddir/new/libidn2-2.3.8.tar.gz`

Phase 1 reason: `expired`

## B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE

- certificates: B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
- found via: hkps://keys.mailvelope.com, hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 5866 → 15923 bytes

```diff
--- dist-git/B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
+++ refreshed/B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
@@ -1,19 +1,17 @@
       Fingerprint: B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
-                   Invalid: The primary key is not live: Expired on 2022-10-23T15:48:28Z
-  Expiration time: 2022-10-23 15:48:28 UTC (creation time + 3years 7months 3days 20h 15m 52s)
+  Expiration time: 2026-11-19 08:55:45 UTC (creation time + 7years 8months 2h 49m 33s)
         Key flags: certification, signing
            Subkey: CA7E37164342DF3133DF349780260EE8A9B92B2B
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-10-23T15:48:28Z
-  Expiration time: 2022-10-23 15:48:43 UTC (creation time + 3years 7months 3days 20h 12m 54s)
+  Expiration time: 2026-11-18 07:59:19 UTC (creation time + 7years 7months 29days 12h 23m 30s)
         Key flags: authentication
            Subkey: A3CC9C870B9D310ABAD4CF2F51722B08FE4745A2
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-10-23T15:48:28Z
-  Expiration time: 2022-10-23 15:48:47 UTC (creation time + 3years 7months 3days 20h 12m 46s)
+  Expiration time: 2026-11-18 07:59:19 UTC (creation time + 7years 7months 29days 12h 23m 18s)
         Key flags: signing
            Subkey: A9EC8F4D7F1E50ED3DEF49A902923D7EE76EBD60
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-10-23T15:48:28Z
-  Expiration time: 2022-10-23 15:48:36 UTC (creation time + 3years 7months 3days 20h 12m 58s)
+  Expiration time: 2026-11-18 07:59:19 UTC (creation time + 7years 7months 29days 12h 23m 41s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Simon Josefsson <simon@josefsson.org>
-self-signatures PositiveCertification: 2019-03-20, 2019-10-23, 2020-05-27, 2020-12-22, 2021-07-21, 2022-03-21
-self-signatures SubkeyBinding: 2019-03-20, 2019-10-23, 2020-05-27, 2020-12-22, 2021-07-21, 2022-03-21
+self-signatures PositiveCertification: 2019-03-20, 2019-10-23, 2020-05-27, 2020-12-22, 2021-07-21, 2022-03-21, 2022-10-04, 2023-09-01, 2024-03-22, 2025-03-12, 2026-04-17
+self-signatures SubkeyBinding: 2019-03-20, 2019-10-23, 2020-05-27, 2020-12-22, 2021-07-21, 2022-03-21, 2022-10-04, 2023-09-01, 2024-03-22, 2025-03-12, 2026-04-16
+third-party GenericCertification: 7
+third-party PositiveCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... libidn2-2.3.8.tar.gz
B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
rc=0
```

