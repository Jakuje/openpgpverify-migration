# Keyring refresh for nettle

**Status: still-fails**

Failing call: `--keyring=/builddir/new/nettle-release-keyring.gpg --signature=/builddir/new/nettle-4.0.tar.gz.sig --data=/builddir/new/nettle-4.0.tar.gz`

Phase 1 reason: `expired`

## nettle-release-keyring.gpg

- certificates: 343C2FF0FBEE5EC2EDBEF399F3599FF828C67298
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 31405 → 32303 bytes

```diff
--- dist-git/nettle-release-keyring.gpg
+++ refreshed/nettle-release-keyring.gpg
@@ -11,6 +11,6 @@
 self-signatures SubkeyBinding: 2013-01-07, 2020-01-17
 third-party CasualCertification: 7
 third-party CertificationRevocation: 1
-third-party GenericCertification: 16
+third-party GenericCertification: 18
 third-party PersonaCertification: 1
 third-party PositiveCertification: 3
```

## Verification with the refreshed keyring

```
$ sqv ... nettle-4.0.tar.gz
Signing key on 343C2FF0FBEE5EC2EDBEF399F3599FF828C67298 is bad:
           The primary key is not live
  because: Expired on 2025-01-15T17:12:43Z
rc=1
```

