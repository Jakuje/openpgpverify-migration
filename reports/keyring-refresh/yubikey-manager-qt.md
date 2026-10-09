# Keyring refresh for yubikey-manager-qt

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-6690D8BC.gpg --signature=/builddir/new/yubikey-manager-qt-1.2.5.tar.gz.sig --data=/builddir/new/yubikey-manager-qt-1.2.5.tar.gz`

Phase 1 reason: `expired`

## gpgkey-6690D8BC.gpg

- certificates: 9E885C0302F9BB9167529C2D5CBA11E6ADC7BCD1
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD
- size: 4274 → 18320 bytes

```diff
--- dist-git/gpgkey-6690D8BC.gpg
+++ refreshed/gpgkey-6690D8BC.gpg
@@ -1,19 +1,16 @@
       Fingerprint: 9E885C0302F9BB9167529C2D5CBA11E6ADC7BCD1
-                   Invalid: The primary key is not live: Expired on 2020-09-16T11:49:44Z
-  Expiration time: 2020-09-16 11:49:44 UTC (creation time + 11months 30days 3h 50m 24s)
+  Expiration time: 2027-07-14 10:07:08 UTC (creation time + 7years 9months 26days 5h 15m)
         Key flags: certification
            Subkey: D6919FBF48C484F3CB7B71CD870B88256690D8BC
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2020-09-16T11:49:44Z
-  Expiration time: 2020-09-16 12:17:43 UTC (creation time + 11months 30days 3h 50m 24s)
+  Expiration time: 2027-07-14 10:08:26 UTC (creation time + 7years 9months 26days 4h 48m 19s)
         Key flags: signing
            Subkey: BBD85659722519CD52316CA699250E21D6F11774
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2020-09-16T11:49:44Z
-  Expiration time: 2020-09-16 11:55:25 UTC (creation time + 11months 30days 3h 50m 24s)
+  Expiration time: 2027-07-14 10:08:26 UTC (creation time + 7years 9months 26days 5h 10m 37s)
         Key flags: transport encryption, data-at-rest encryption
            Subkey: 95D3D9E90BA66C89CEA7838DF401E8A14F5D4E60
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2020-09-16T11:49:44Z
-  Expiration time: 2020-09-16 12:20:37 UTC (creation time + 11months 30days 3h 50m 24s)
+  Expiration time: 2027-07-14 10:08:26 UTC (creation time + 7years 9months 26days 4h 45m 25s)
         Key flags: authentication
            UserID: Dennis Fokin <dennis.fokin@yubico.com>
-self-signatures PositiveCertification: 2019-09-17
-self-signatures SubkeyBinding: 2019-09-17
+self-signatures PositiveCertification: 2019-09-17, 2020-09-14, 2021-09-07, 2022-09-07, 2023-08-02, 2025-07-14
+self-signatures SubkeyBinding: 2019-09-17, 2020-09-14, 2021-09-07, 2022-09-07, 2023-08-02, 2025-07-14
+third-party GenericCertification: 2
```

## Verification with the refreshed keyring

```
$ sqv ... yubikey-manager-qt-1.2.5.tar.gz
9E885C0302F9BB9167529C2D5CBA11E6ADC7BCD1
rc=0
```

