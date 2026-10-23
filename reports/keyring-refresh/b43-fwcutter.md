# Keyring refresh for b43-fwcutter

**Status: proposed**

Failing call: `--keyring=/builddir/new/757FAB7CED1814AE15B4836E5FB027474203454C.gpg --signature=/builddir/new/b43-fwcutter-021.tar.xz.asc --data=/builddir/new/b43-fwcutter-021.tar.xz`

Phase 1 reason: `expired`

## 757FAB7CED1814AE15B4836E5FB027474203454C.gpg

- certificates: 0392335A78083894A4301C43236E8A58C6DB4512, 69100FFB90E87A320DF8643CBEC39009E8321A61, 757FAB7CED1814AE15B4836E5FB027474203454C
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 29671 → 42386 bytes

```diff
--- dist-git/757FAB7CED1814AE15B4836E5FB027474203454C.gpg
+++ refreshed/757FAB7CED1814AE15B4836E5FB027474203454C.gpg
@@ -25,14 +25,13 @@
         Key flags: transport encryption, data-at-rest encryption
            UserID: Ivan Alonso [Kaian] <kaian@irontec.com>
       Fingerprint: 757FAB7CED1814AE15B4836E5FB027474203454C
-                   Invalid: The primary key is not live: Expired on 2026-06-14T18:23:49Z
-  Expiration time: 2026-06-14 18:23:49 UTC (creation time + 14years 3months 24days 8h 21m 9s)
+  Expiration time: 2027-06-14 18:46:36 UTC (creation time + 15years 3months 24days 2h 43m 56s)
         Key flags: certification, signing
            Subkey: BC87DDC8C8254346D5F62B400988558F3A32F21D
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-06-14T18:23:49Z
-  Expiration time: 2026-06-14 18:24:26 UTC (creation time + 14years 3months 24days 8h 21m 46s)
+  Expiration time: 2027-06-14 18:46:47 UTC (creation time + 15years 3months 24days 2h 44m 7s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Michael Büsch (Git tag signing key) <m@bues.ch>
            UserID: Michael Büsch (Release signing key) <m@bues.ch>
-self-signatures PositiveCertification: 2012-02-19, 2013-03-01, 2013-08-10, 2014-03-02, 2015-03-04, 2016-03-03, 2018-01-09, 2018-03-03, 2019-03-02, 2020-02-22, 2020-05-21, 2021-03-31, 2023-04-15, 2024-04-16, 2025-06-14, 2025-10-16
-self-signatures SubkeyBinding: 2013-08-10, 2020-05-21, 2025-06-14
+self-signatures PositiveCertification: 2012-02-19, 2013-03-01, 2013-08-10, 2014-03-02, 2015-03-04, 2016-03-03, 2018-01-09, 2018-03-03, 2019-03-02, 2020-02-22, 2020-05-21, 2021-03-31, 2023-04-15, 2024-04-16, 2025-06-14, 2025-10-16, 2026-06-14
+self-signatures SubkeyBinding: 2012-02-19, 2013-03-01, 2013-08-10, 2014-03-02, 2015-03-04, 2016-03-03, 2018-01-09, 2018-03-03, 2019-03-02, 2020-02-22, 2020-05-21, 2021-03-31, 2023-04-15, 2024-04-16, 2025-06-14, 2026-06-14
+third-party GenericCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... b43-fwcutter-021.tar.xz
757FAB7CED1814AE15B4836E5FB027474203454C
rc=0
```

