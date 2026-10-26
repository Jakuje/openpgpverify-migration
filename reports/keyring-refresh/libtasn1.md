# Keyring refresh for libtasn1

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE.gpg --signature=/builddir/new/libtasn1-4.21.0.tar.gz.sig --data=/builddir/new/libtasn1-4.21.0.tar.gz`

Phase 1 reason: `expired`

## gpgkey-B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE.gpg

- certificates: B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
- found via: hkps://keys.mailvelope.com, hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 911 → 12355 bytes

```diff
--- dist-git/gpgkey-B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE.gpg
+++ refreshed/gpgkey-B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE.gpg
@@ -1,19 +1,17 @@
       Fingerprint: B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
-                   Invalid: The primary key is not live: Expired on 2022-05-17T06:38:35Z
-  Expiration time: 2022-05-17 06:38:35 UTC (creation time + 3years 1month 27days 2h 27m 35s)
+  Expiration time: 2027-05-24 20:19:03 UTC (creation time + 8years 2months 3days 23h 34m 27s)
         Key flags: certification, signing
            Subkey: A3CC9C870B9D310ABAD4CF2F51722B08FE4745A2
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-05-17T06:38:35Z
-  Expiration time: 2022-05-17 06:38:50 UTC (creation time + 3years 1month 27days 2h 24m 25s)
+  Expiration time: 2027-05-24 20:14:47 UTC (creation time + 8years 2months 3days 23h 26m 46s)
         Key flags: signing
            Subkey: A9EC8F4D7F1E50ED3DEF49A902923D7EE76EBD60
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-05-17T06:38:35Z
-  Expiration time: 2022-05-17 06:38:41 UTC (creation time + 3years 1month 27days 2h 24m 39s)
+  Expiration time: 2027-05-24 20:14:47 UTC (creation time + 8years 2months 3days 23h 27m 9s)
         Key flags: transport encryption, data-at-rest encryption
            Subkey: CA7E37164342DF3133DF349780260EE8A9B92B2B
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-05-17T06:38:35Z
-  Expiration time: 2022-05-17 06:38:46 UTC (creation time + 3years 1month 27days 2h 24m 33s)
+  Expiration time: 2027-05-24 20:14:47 UTC (creation time + 8years 2months 3days 23h 26m 58s)
         Key flags: authentication
            UserID: Simon Josefsson <simon@josefsson.org>
-self-signatures PositiveCertification: 2021-07-21
-self-signatures SubkeyBinding: 2021-07-21
+self-signatures PositiveCertification: 2019-03-20, 2019-10-23, 2020-05-27, 2020-12-22, 2021-07-21, 2022-03-21, 2022-10-04, 2023-09-01, 2024-03-22, 2025-03-12, 2026-04-17, 2026-10-20
+self-signatures SubkeyBinding: 2019-03-20, 2019-10-23, 2020-05-27, 2020-12-22, 2021-07-21, 2022-03-21, 2022-10-04, 2023-09-01, 2024-03-22, 2025-03-12, 2026-04-16, 2026-10-20
+third-party GenericCertification: 7
+third-party PositiveCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... libtasn1-4.21.0.tar.gz
B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
rc=0
```

