# Keyring update from upstream for openresolv

**Status: proposed**

Failing call: `--keyring=/builddir/new/roy.marples.asc --signature=/builddir/new/openresolv-3.17.4.tar.xz.asc --data=/builddir/new/openresolv-3.17.4.tar.xz`

Phase 1 reason: `sha1-cert`

## roy.marples.asc

- from: http://keyserver.ubuntu.com/pks/lookup?op=get&search=0xa785ed2755955d9e93ea59f6597f97ea9ad45549
- certificates (unchanged): A785ED2755955D9E93EA59F6597F97EA9AD45549
- size: 3843 → 6420 bytes

```
curl -fsSL -o roy.marples.asc http://keyserver.ubuntu.com/pks/lookup?op=get&search=0xa785ed2755955d9e93ea59f6597f97ea9ad45549
```

```diff
--- dist-git/roy.marples.asc
+++ upstream/roy.marples.asc
@@ -1,15 +1,10 @@
       Fingerprint: A785ED2755955D9E93EA59F6597F97EA9AD45549
-                   Invalid: No binding signature at time 2026-10-27T11:31:31Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: E9EE92F5F6D5DBE878B3C2690B0EEE0F057A64CF
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-27T11:31:31Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Roy Marples (NetBSD) <roy@NetBSD.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Roy Marples <roy@marples.name>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2008-11-24, 2008-12-09, 2010-02-20
-self-signatures SubkeyBinding: 2008-11-24
+self-signatures PositiveCertification: 2008-11-24, 2008-12-09, 2010-02-20, 2023-04-24, 2023-04-25
+self-signatures SubkeyBinding: 2008-11-24, 2023-04-24
+third-party CasualCertification: 1
 third-party PositiveCertification: 2
```

## Verification with the upstream keyring

```
$ sqv ... openresolv-3.17.4.tar.xz
A785ED2755955D9E93EA59F6597F97EA9AD45549
rc=0
```

