# Keyring refresh for slrn

**Status: still-fails**

Failing call: `--keyring=/builddir/new/slrn-gpgkeys.gpg --signature=/builddir/new/slrn-1.0.3a.tar.bz2.asc --data=/builddir/new/slrn-1.0.3a.tar.bz2`

Phase 1 reason: `v3-sig`

## slrn-gpgkeys.gpg

- certificates: AE962A02D29BFE4A4BB2805FDE401E0D5873000A
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 963 → 1181 bytes

```diff
--- dist-git/slrn-gpgkeys.gpg
+++ refreshed/slrn-gpgkeys.gpg
@@ -7,6 +7,9 @@
            UserID: John E. Davis <davis@space.mit.edu>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2004-09-19
+           UserID: John E. Davis <jed@jedsoft.org>
+                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
+self-signatures PositiveCertification: 2004-09-19, 2006-01-16
 self-signatures SubkeyBinding: 2004-09-19
 third-party GenericCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... slrn-1.0.3a.tar.bz2
Error: Policy rejected packet type

Caused by:
    Signature Packet v3 is not considered secure since 2021-02-01T00:00:00Z
rc=1
```

