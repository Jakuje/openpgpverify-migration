# Keyring refresh for time

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-F576AAAC1B0FF849792D8CB129A794FD2272BC86.gpg --signature=/builddir/new/time-1.9.tar.gz.sig --data=/builddir/new/time-1.9.tar.gz`

Phase 1 reason: `unknown`

## gpgkey-F576AAAC1B0FF849792D8CB129A794FD2272BC86.gpg

- certificates: F576AAAC1B0FF849792D8CB129A794FD2272BC86
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 4529 → 15576 bytes

```diff
--- dist-git/gpgkey-F576AAAC1B0FF849792D8CB129A794FD2272BC86.gpg
+++ refreshed/gpgkey-F576AAAC1B0FF849792D8CB129A794FD2272BC86.gpg
@@ -12,5 +12,4 @@
         Key flags: transport encryption, data-at-rest encryption
            UserID: Assaf Gordon <agordon@wi.mit.edu>
                    Revoked:
-                   Invalid: No binding signature at time 2026-10-08T13:05:44Z
            UserID: Assaf Gordon <assafgordon@gmail.com>
```

## Verification with the refreshed keyring

```
$ sqv ... time-1.9.tar.gz
F576AAAC1B0FF849792D8CB129A794FD2272BC86
rc=0
```

