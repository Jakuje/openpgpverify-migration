# Keyring refresh for oath-toolkit

**Status: proposed**

Failing call: `--keyring=/builddir/new/keyring.asc --signature=/builddir/new/oath-toolkit-2.6.15.tar.gz.sig --data=/builddir/new/oath-toolkit-2.6.15.tar.gz`

Phase 1 reason: `expired`

## keyring.asc

- certificates: B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
- found via: hkps://keys.mailvelope.com, hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 1314 → 16813 bytes

```diff
--- dist-git/keyring.asc
+++ refreshed/keyring.asc
@@ -1,19 +1,17 @@
       Fingerprint: B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
-                   Invalid: The primary key is not live: Expired on 2025-04-26T13:30:48Z
-  Expiration time: 2025-04-26 13:30:48 UTC (creation time + 6years 1month 6days 15h 19m 48s)
+  Expiration time: 2027-05-24 20:19:03 UTC (creation time + 8years 2months 3days 23h 34m 27s)
         Key flags: certification, signing
            Subkey: A3CC9C870B9D310ABAD4CF2F51722B08FE4745A2
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-04-26T13:30:48Z
-  Expiration time: 2025-04-26 13:31:23 UTC (creation time + 6years 1month 6days 15h 16m 58s)
+  Expiration time: 2027-05-24 20:14:47 UTC (creation time + 8years 2months 3days 23h 26m 46s)
         Key flags: signing
            Subkey: A9EC8F4D7F1E50ED3DEF49A902923D7EE76EBD60
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-04-26T13:30:48Z
-  Expiration time: 2025-04-26 13:31:28 UTC (creation time + 6years 1month 6days 15h 17m 26s)
+  Expiration time: 2027-05-24 20:14:47 UTC (creation time + 8years 2months 3days 23h 27m 9s)
         Key flags: transport encryption, data-at-rest encryption
            Subkey: CA7E37164342DF3133DF349780260EE8A9B92B2B
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-04-26T13:30:48Z
-  Expiration time: 2025-04-26 13:31:16 UTC (creation time + 6years 1month 6days 15h 17m 3s)
+  Expiration time: 2027-05-24 20:14:47 UTC (creation time + 8years 2months 3days 23h 26m 58s)
         Key flags: authentication
            UserID: Simon Josefsson <simon@josefsson.org>
-self-signatures PositiveCertification: 2024-03-22
-self-signatures SubkeyBinding: 2024-03-22
+self-signatures PositiveCertification: 2019-03-20, 2019-10-23, 2020-05-27, 2020-12-22, 2021-07-21, 2022-03-21, 2022-10-04, 2023-09-01, 2024-03-22, 2025-03-12, 2026-04-17, 2026-10-20
+self-signatures SubkeyBinding: 2019-03-20, 2019-10-23, 2020-05-27, 2020-12-22, 2021-07-21, 2022-03-21, 2022-10-04, 2023-09-01, 2024-03-22, 2025-03-12, 2026-04-16, 2026-10-20
+third-party GenericCertification: 7
+third-party PositiveCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... oath-toolkit-2.6.15.tar.gz
B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
rc=0
```

