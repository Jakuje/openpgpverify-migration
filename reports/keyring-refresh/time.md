# Keyring refresh for time

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-F576AAAC1B0FF849792D8CB129A794FD2272BC86.gpg --signature=/builddir/new/time-1.9.tar.gz.sig --data=/builddir/new/time-1.9.tar.gz`

Phase 1 reason: `binding-after-signature`

## gpgkey-F576AAAC1B0FF849792D8CB129A794FD2272BC86.gpg

- certificates: F576AAAC1B0FF849792D8CB129A794FD2272BC86
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 4529 → 15576 bytes

```diff
--- dist-git/gpgkey-F576AAAC1B0FF849792D8CB129A794FD2272BC86.gpg
+++ refreshed/gpgkey-F576AAAC1B0FF849792D8CB129A794FD2272BC86.gpg
@@ -12,8 +12,8 @@
         Key flags: transport encryption, data-at-rest encryption
            UserID: Assaf Gordon <agordon@wi.mit.edu>
                    Revoked:
-                   Invalid: No binding signature at time 2026-10-09T13:01:20Z
            UserID: Assaf Gordon <assafgordon@gmail.com>
 self-signatures CertificationRevocation: 2015-08-13
-self-signatures PositiveCertification: 2020-02-24
-self-signatures SubkeyBinding: 2020-02-24
+self-signatures PositiveCertification: 2014-07-09, 2015-08-12, 2017-01-19, 2018-02-14, 2020-02-24
+self-signatures SubkeyBinding: 2014-07-09, 2015-08-12, 2017-01-19, 2018-02-14, 2020-02-24
+third-party GenericCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... time-1.9.tar.gz
F576AAAC1B0FF849792D8CB129A794FD2272BC86
rc=0
```

