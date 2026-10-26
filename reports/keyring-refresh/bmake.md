# Keyring refresh for bmake

**Status: still-fails**

Failing call: `--keyring=/builddir/new/Crufty.pub.asc --signature=/builddir/new/bmake-20230711.tar.gz.asc --data=/builddir/new/bmake-20230711.tar.gz`

Phase 1 reason: `sha1-cert`

## Crufty.pub.asc

- certificates: 7E228507C26D8DC164F531BFBA54C8AF755A2A99
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 2070 → 3484 bytes

```diff
--- dist-git/Crufty.pub.asc
+++ refreshed/Crufty.pub.asc
@@ -1,7 +1,10 @@
       Fingerprint: 7E228507C26D8DC164F531BFBA54C8AF755A2A99
                    Invalid: No binding signature at time 2026-10-26T17:08:31Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+           UserID: Crufty.NET
+                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
            UserID: sigs (OpenPGP) <sigs@crufty.net>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2021-04-27
-third-party GenericCertification: 1
+self-signatures PositiveCertification: 2021-04-26, 2021-04-27
+third-party GenericCertification: 2
```

## Verification with the refreshed keyring

```
$ sqv ... bmake-20230711.tar.gz
Signing key on 7E228507C26D8DC164F531BFBA54C8AF755A2A99 is not bound:
           No binding signature at time 2023-07-19T00:06:12Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

