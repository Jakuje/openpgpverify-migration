# Keyring refresh for openresolv

**Status: proposed**

Failing call: `--keyring=/builddir/new/roy.marples.asc --signature=/builddir/new/openresolv-3.17.4.tar.xz.asc --data=/builddir/new/openresolv-3.17.4.tar.xz`

Phase 1 reason: `sha1-cert`

## roy.marples.asc

- certificates: A785ED2755955D9E93EA59F6597F97EA9AD45549
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 3843 → 6470 bytes

```diff
--- dist-git/roy.marples.asc
+++ refreshed/roy.marples.asc
@@ -1,12 +1,6 @@
       Fingerprint: A785ED2755955D9E93EA59F6597F97EA9AD45549
-                   Invalid: No binding signature at time 2026-10-08T12:10:10Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: E9EE92F5F6D5DBE878B3C2690B0EEE0F057A64CF
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-08T12:10:10Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Roy Marples (NetBSD) <roy@NetBSD.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Roy Marples <roy@marples.name>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
```

## Verification with the refreshed keyring

```
$ sqv ... openresolv-3.17.4.tar.xz
A785ED2755955D9E93EA59F6597F97EA9AD45549
rc=0
```

