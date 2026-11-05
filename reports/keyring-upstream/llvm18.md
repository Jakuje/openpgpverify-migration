# Keyring update from upstream for llvm18

**Status: proposed**

Failing call: `--keyring=/builddir/new/release-keys.asc --signature=/builddir/new/llvm-18.1.8.src.tar.xz.sig --data=/builddir/new/llvm-18.1.8.src.tar.xz`

Phase 1 reason: `expired`

## release-keys.asc

- from: https://releases.llvm.org/release-keys.asc
- **adds keys the URL also holds: B6C8F98282B944E3B0D5C2530FC3042E345AD05D, 0FB96824606D15FDD54C3D092FFC629D3F563BDC, 71046D1E9C6656BDD61171873E83BABF4A4F9E85, FFB3368980F3E6BB5737145A316C56D064CACBA5** (asked for)
- certificates (unchanged): D574BD5D1D0E98895E3BF90044F2485E45D59042, 474E22316ABF4785A88C6E8EA2C794A986419D8A
- size: 6354 → 13300 bytes

```
curl -fsSL -O https://releases.llvm.org/release-keys.asc
```

```diff
--- dist-git/release-keys.asc
+++ upstream/release-keys.asc
@@ -6,13 +6,39 @@
         Key flags: transport encryption, data-at-rest encryption
            UserID: Tobias Hieta <tobias@hieta.se>
       Fingerprint: 474E22316ABF4785A88C6E8EA2C794A986419D8A
-                   Invalid: The primary key is not live: Expired on 2023-05-05T23:33:51Z
-  Expiration time: 2023-05-05 23:33:51 UTC (creation time + 5years 2days 14h 8m 2s)
+                   Invalid: The primary key is not live: Expired on 2025-05-02T17:49:59Z
+  Expiration time: 2025-05-02 17:49:59 UTC (creation time + 6years 11months 30days 6h 14m 34s)
         Key flags: certification, signing
            Subkey: 6717A17756AD71AA42B7E6660AE0D586997F0D1F
+                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-05-02T17:49:59Z
+  Expiration time: 2025-05-02 17:51:32 UTC (creation time + 6years 11months 30days 6h 16m 7s)
+        Key flags: transport encryption, data-at-rest encryption
+           UserID: Tom Stellard <tstellar@redhat.com>
+      Fingerprint: B6C8F98282B944E3B0D5C2530FC3042E345AD05D
+  Expiration time: 2029-10-15 09:20:01 UTC (creation time + 14years 8months 24days 10h 28m 49s)
+        Key flags: certification, signing
+           Subkey: A7F1C1CD2428B2B66C09AD8E3276ABBAE8E36D78
+  Expiration time: 2029-10-15 09:20:55 UTC (creation time + 10years 6months 11days 21h 8m 23s)
+        Key flags: transport encryption, data-at-rest encryption
+           Subkey: C569F42EE903DB0A0AB4B1768514EA9C9330FC0D
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
-           UserID: Tom Stellard <tstellar@redhat.com>
-self-signatures PositiveCertification: 2018-05-03, 2021-05-05, 2022-08-05
-self-signatures SubkeyBinding: 2018-05-03, 2022-08-05
+           UserID: Hans Wennborg <hans@chromium.org>
+      Fingerprint: 0FB96824606D15FDD54C3D092FFC629D3F563BDC
+        Key flags: certification, signing
+           Subkey: 295E95E904B8FFCE900EF7B2256F54DAEDBE640D
+        Key flags: transport encryption, data-at-rest encryption
+           UserID: Muhammad Omair Javaid (LLVM Release Signing Key) <omair.javaid@linaro.org>
+      Fingerprint: 71046D1E9C6656BDD61171873E83BABF4A4F9E85
+        Key flags: certification, signing
+           Subkey: FC375C4C3D0910B7856F6FD8DB76C32D7B72878B
+        Key flags: transport encryption, data-at-rest encryption
+           UserID: Cullen Rhodes <cullen.rhodes@arm.com>
+      Fingerprint: FFB3368980F3E6BB5737145A316C56D064CACBA5
+        Key flags: certification, signing
+           Subkey: 1FE1C822C37D38862D36BBE9B977855DC9580AA9
+        Key flags: transport encryption, data-at-rest encryption
+           UserID: Douglas Yung <douglas.yung@sony.com>
+self-signatures PositiveCertification: 2018-05-03, 2022-08-05, 2024-05-02, 2024-10-15, 2024-10-16, 2025-09-15
+self-signatures SubkeyBinding: 2018-01-16, 2022-08-05, 2024-05-02, 2024-10-15, 2024-10-16, 2025-09-15
```

## Verification with the upstream keyring

```
$ sqv ... llvm-18.1.8.src.tar.xz
474E22316ABF4785A88C6E8EA2C794A986419D8A
rc=0
```

