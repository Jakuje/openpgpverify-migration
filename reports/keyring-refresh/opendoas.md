# Keyring refresh for opendoas

**Status: still-fails**

Failing call: `--keyring=/builddir/new/duncan.asc --signature=/builddir/new/opendoas-6.8.2.tar.gz.sig --data=/builddir/new/opendoas-6.8.2.tar.gz`

Phase 1 reason: `expired`

## duncan.asc

- certificates: C4B6FBA98211F7EFF35DEB73335C1D17EC3D6E35
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 6271 → 19831 bytes

```diff
--- dist-git/duncan.asc
+++ refreshed/duncan.asc
@@ -1,16 +1,16 @@
       Fingerprint: C4B6FBA98211F7EFF35DEB73335C1D17EC3D6E35
-                   Invalid: The primary key is not live: Expired on 2022-01-11T22:22:04Z
-  Expiration time: 2022-01-11 22:22:04 UTC (creation time + 4years 9months 25days 6h 41m 13s)
+                   Invalid: The primary key is not live: Expired on 2026-01-13T18:12:10Z
+  Expiration time: 2026-01-13 18:12:10 UTC (creation time + 8years 9months 27days 2h 31m 19s)
         Key flags: certification, signing
            Subkey: 7BF63D7EABF41506AE50FCC1AAE55DC91A8315F7
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-01-11T22:22:04Z
-  Expiration time: 2021-01-10 22:47:34 UTC (creation time + 3years 9months 24days 13h 6m 43s)
+                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-01-13T18:12:10Z
+  Expiration time: 2026-01-13 18:12:27 UTC (creation time + 8years 9months 27days 2h 31m 36s)
         Key flags: transport encryption, data-at-rest encryption
            Subkey: DF8FEBAEA70A5A692AA809F5EB132ADCA5893D37
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-01-11T22:22:04Z
-  Expiration time: 2022-08-09 16:20:53 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-01-13T18:12:10Z
+  Expiration time: 2026-01-13 18:12:27 UTC (creation time + 5years 5months 4days 15h 3m 34s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Duncaen <duncaen@voidlinux.org>
            UserID: Duncan Overbruck <mail@duncano.de>
-self-signatures PositiveCertification: 2017-03-18, 2021-01-11
-self-signatures SubkeyBinding: 2019-01-11, 2020-08-09
+self-signatures PositiveCertification: 2017-03-18, 2019-01-11, 2019-11-06, 2021-01-11, 2023-01-12, 2024-01-13, 2025-01-13
+self-signatures SubkeyBinding: 2019-01-11, 2020-08-09, 2023-01-12, 2024-01-13, 2025-01-13
```

## Verification with the refreshed keyring

```
$ sqv ... opendoas-6.8.2.tar.gz
Signing key on C4B6FBA98211F7EFF35DEB73335C1D17EC3D6E35 is bad:
           The primary key is not live
  because: Expired on 2022-01-11T22:22:04Z
rc=1
```

