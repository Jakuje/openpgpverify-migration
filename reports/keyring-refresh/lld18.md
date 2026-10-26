# Keyring refresh for lld18

**Status: proposed**

Failing call: `--keyring=/builddir/new/release-keys.asc --signature=/builddir/new/lld-18.1.8.src.tar.xz.sig --data=/builddir/new/lld-18.1.8.src.tar.xz`

Phase 1 reason: `expired`

## release-keys.asc

- certificates: D574BD5D1D0E98895E3BF90044F2485E45D59042, 474E22316ABF4785A88C6E8EA2C794A986419D8A
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 6354 → 12612 bytes

```diff
--- dist-git/release-keys.asc
+++ refreshed/release-keys.asc
@@ -6,13 +6,13 @@
         Key flags: transport encryption, data-at-rest encryption
            UserID: Tobias Hieta <tobias@hieta.se>
       Fingerprint: 474E22316ABF4785A88C6E8EA2C794A986419D8A
-                   Invalid: The primary key is not live: Expired on 2023-05-05T23:33:51Z
-  Expiration time: 2023-05-05 23:33:51 UTC (creation time + 5years 2days 14h 8m 2s)
+                   Invalid: The primary key is not live: Expired on 2026-05-06T21:16:35Z
+  Expiration time: 2026-05-06 21:16:35 UTC (creation time + 8years 3days 17h 50m 46s)
         Key flags: certification, signing
            Subkey: 6717A17756AD71AA42B7E6660AE0D586997F0D1F
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
+                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-05-06T21:16:35Z
+  Expiration time: 2026-05-06 22:13:22 UTC (creation time + 8years 3days 18h 47m 33s)
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Tom Stellard <tstellar@redhat.com>
-self-signatures PositiveCertification: 2018-05-03, 2021-05-05, 2022-08-05
-self-signatures SubkeyBinding: 2018-05-03, 2022-08-05
+self-signatures PositiveCertification: 2018-05-03, 2019-05-02, 2021-05-05, 2022-08-05, 2023-05-17, 2024-05-02, 2025-05-06
+self-signatures SubkeyBinding: 2018-05-03, 2022-08-05, 2023-04-18, 2024-01-13, 2024-05-02, 2025-05-06
```

## Verification with the refreshed keyring

```
$ sqv ... lld-18.1.8.src.tar.xz
474E22316ABF4785A88C6E8EA2C794A986419D8A
rc=0
```

