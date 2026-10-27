# Keyring refresh for llvm14

**Status: proposed**

Failing call: `--keyring=/builddir/new/tstellar-gpg-key.asc --signature=/builddir/new/llvm-14.0.5.src.tar.xz.sig --data=/builddir/new/llvm-14.0.5.src.tar.xz`

Phase 1 reason: `sha1-cert`

## tstellar-gpg-key.asc

- certificates: 474E22316ABF4785A88C6E8EA2C794A986419D8A
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 2222 → 7504 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network search --output - 474E22316ABF4785A88C6E8EA2C794A986419D8A \
  | sq keyring filter --experimental --cert 474E22316ABF4785A88C6E8EA2C794A986419D8A --output update.pgp
sq keyring merge tstellar-gpg-key.asc update.pgp | sq packet dearmor --output tstellar-gpg-key.asc.new
mv tstellar-gpg-key.asc.new tstellar-gpg-key.asc
```

```diff
--- dist-git/tstellar-gpg-key.asc
+++ refreshed/tstellar-gpg-key.asc
@@ -1,11 +1,11 @@
       Fingerprint: 474E22316ABF4785A88C6E8EA2C794A986419D8A
-                   Invalid: No binding signature at time 2026-10-27T10:59:09Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: The primary key is not live: Expired on 2026-05-06T21:16:35Z
+  Expiration time: 2026-05-06 21:16:35 UTC (creation time + 8years 3days 17h 50m 46s)
+        Key flags: certification, signing
            Subkey: 6717A17756AD71AA42B7E6660AE0D586997F0D1F
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-27T10:59:09Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-05-06T21:16:35Z
+  Expiration time: 2026-05-06 22:13:22 UTC (creation time + 8years 3days 18h 47m 33s)
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Tom Stellard <tstellar@redhat.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2018-05-03
-self-signatures SubkeyBinding: 2018-05-03
+self-signatures PositiveCertification: 2018-05-03, 2019-05-02, 2021-05-05, 2023-05-17, 2024-05-02, 2025-05-06
+self-signatures SubkeyBinding: 2018-05-03, 2023-04-18, 2024-01-13, 2024-05-02, 2025-05-06
```

## Verification with the refreshed keyring

```
$ sqv ... llvm-14.0.5.src.tar.xz
474E22316ABF4785A88C6E8EA2C794A986419D8A
rc=0
```

