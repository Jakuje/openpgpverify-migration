# Keyring refresh for coreutils

**Status: still-fails**

Failing call: `--keyring=/builddir/new/coreutils-keyring.gpg --signature=/builddir/new/coreutils-9.12.tar.xz.sig --data=/builddir/new/coreutils-9.12.tar.xz`

Phase 1 reason: `sha1-cert`

## coreutils-keyring.gpg

- certificates: 6C37DC12121A5006BC1DB804DF6FD971306037D9
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 20290 → 17508 bytes

```diff
--- dist-git/coreutils-keyring.gpg
+++ refreshed/coreutils-keyring.gpg
@@ -8,7 +8,8 @@
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
            UserID: Pádraig Brady <pbrady@redhat.com>
-                   Invalid: No binding signature at time 2026-10-12T11:54:59Z
+                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
            UserID: Pádraig Brady <pixelbeat@gnu.org>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
```

## Verification with the refreshed keyring

```
$ sqv ... coreutils-9.12.tar.xz
Signing key on 6C37DC12121A5006BC1DB804DF6FD971306037D9 is not bound:
           No binding signature at time 2026-09-14T15:37:50Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

