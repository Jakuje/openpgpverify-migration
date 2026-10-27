# Keyring update from upstream for libidn2

**Status: proposed**

Failing call: `--keyring=/builddir/new/B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE --signature=/builddir/new/libidn2-2.3.8.tar.gz.sig --data=/builddir/new/libidn2-2.3.8.tar.gz`

Phase 1 reason: `expired`

## B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE

- from: https://keys.openpgp.org/vks/v1/by-fingerprint/B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
- certificates (unchanged): B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
- size: 5866 → 10513 bytes

```
curl -fsSL -o B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE https://keys.openpgp.org/vks/v1/by-fingerprint/B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
```

```diff
--- dist-git/B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
+++ upstream/B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
@@ -1,19 +1,15 @@
       Fingerprint: B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
-                   Invalid: The primary key is not live: Expired on 2022-10-23T15:48:28Z
-  Expiration time: 2022-10-23 15:48:28 UTC (creation time + 3years 7months 3days 20h 15m 52s)
+  Expiration time: 2027-05-24 20:19:03 UTC (creation time + 8years 2months 3days 23h 34m 27s)
         Key flags: certification, signing
            Subkey: A3CC9C870B9D310ABAD4CF2F51722B08FE4745A2
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-10-23T15:48:28Z
-  Expiration time: 2022-10-23 15:48:47 UTC (creation time + 3years 7months 3days 20h 12m 46s)
+  Expiration time: 2027-05-24 20:14:47 UTC (creation time + 8years 2months 3days 23h 26m 46s)
         Key flags: signing
            Subkey: A9EC8F4D7F1E50ED3DEF49A902923D7EE76EBD60
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-10-23T15:48:28Z
-  Expiration time: 2022-10-23 15:48:36 UTC (creation time + 3years 7months 3days 20h 12m 58s)
+  Expiration time: 2027-05-24 20:14:47 UTC (creation time + 8years 2months 3days 23h 27m 9s)
         Key flags: transport encryption, data-at-rest encryption
            Subkey: CA7E37164342DF3133DF349780260EE8A9B92B2B
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-10-23T15:48:28Z
-  Expiration time: 2022-10-23 15:48:43 UTC (creation time + 3years 7months 3days 20h 12m 54s)
+  Expiration time: 2027-05-24 20:14:47 UTC (creation time + 8years 2months 3days 23h 26m 58s)
         Key flags: authentication
            UserID: Simon Josefsson <simon@josefsson.org>
-self-signatures PositiveCertification: 2019-03-20, 2019-10-23, 2020-05-27, 2020-12-22, 2021-07-21, 2022-03-21
-self-signatures SubkeyBinding: 2019-03-20, 2019-10-23, 2020-05-27, 2020-12-22, 2021-07-21, 2022-03-21
+self-signatures PositiveCertification: 2019-03-20, 2019-10-23, 2020-05-27, 2020-12-22, 2021-07-21, 2022-03-21, 2022-10-04, 2023-09-01, 2024-03-22, 2025-03-12, 2026-04-17, 2026-10-20
+self-signatures SubkeyBinding: 2019-03-20, 2019-10-23, 2020-05-27, 2020-12-22, 2021-07-21, 2022-03-21, 2022-10-04, 2024-03-22, 2025-03-12, 2026-04-16, 2026-10-20
```

## Verification with the upstream keyring

```
$ sqv ... libidn2-2.3.8.tar.gz
B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
rc=0
```

