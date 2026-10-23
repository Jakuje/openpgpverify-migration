# Keyring refresh for yascreen

**Status: proposed**

Failing call: `--keyring=/builddir/new/signing-key.asc --signature=/builddir/new/yascreen-2.14.tar.xz.asc --data=/builddir/new/yascreen-2.14.tar.xz`

Phase 1 reason: `expired`

## signing-key.asc

- certificates: BA60BC20F37E59444D6D25001365720913D2F22D
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 12848 → 52311 bytes

```diff
--- dist-git/signing-key.asc
+++ refreshed/signing-key.asc
@@ -1,13 +1,13 @@
       Fingerprint: BA60BC20F37E59444D6D25001365720913D2F22D
-                   Invalid: The primary key is not live: Expired on 2023-01-30T18:12:31Z
-  Expiration time: 2023-01-30 18:12:31 UTC (creation time + 2years 7months 3days 5h 15m 7s)
+  Expiration time: 2028-07-20 06:06:24 UTC (creation time + 8years 22days 7h 4m 12s)
         Key flags: certification, signing
            Subkey: 5A7BF57ECE76D83A42B1CA620F9A14812426B4F9
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2023-01-30T18:12:31Z
-  Expiration time: 2023-01-30 18:13:04 UTC (creation time + 2years 7months 3days 5h 15m 40s)
+  Expiration time: 2028-07-20 06:07:52 UTC (creation time + 8years 22days 7h 5m 40s)
         Key flags: transport encryption, data-at-rest encryption
+           UserID: Boian Bonev <bbonev@devuan.org>
            UserID: Boian Bonev <bbonev@ipacct.com>
            UserID: Boian Bonev <boian@bonev.com>
            UserID: Boian Bonev <ipacct@gmail.com>
-self-signatures PositiveCertification: 2020-06-27, 2021-01-30, 2021-02-01
-self-signatures SubkeyBinding: 2020-06-27, 2021-01-30
+self-signatures PositiveCertification: 2020-06-27, 2021-01-30, 2021-02-01, 2022-07-18, 2022-11-04, 2024-02-10, 2025-01-15, 2026-01-21, 2026-07-21
+self-signatures SubkeyBinding: 2020-06-27, 2021-01-30, 2022-07-18, 2024-02-10, 2025-01-15, 2026-01-21, 2026-07-21
+third-party GenericCertification: 9
```

## Verification with the refreshed keyring

```
$ sqv ... yascreen-2.14.tar.xz
BA60BC20F37E59444D6D25001365720913D2F22D
rc=0
```

