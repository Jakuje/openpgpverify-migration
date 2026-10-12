# Keyring refresh for voikko-fi

**Status: still-fails**

Failing call: `--keyring=/builddir/new/gpgkey-AC5D65F10C8596D7E2DAE2633D309B604AE3942E.gpg --signature=/builddir/new/voikko-fi-2.5.tar.gz.asc --data=/builddir/new/voikko-fi-2.5.tar.gz`

Phase 1 reason: `sha1-cert`

## gpgkey-AC5D65F10C8596D7E2DAE2633D309B604AE3942E.gpg

- certificates: AC5D65F10C8596D7E2DAE2633D309B604AE3942E
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 3432 → 3504 bytes

```diff
--- dist-git/gpgkey-AC5D65F10C8596D7E2DAE2633D309B604AE3942E.gpg
+++ refreshed/gpgkey-AC5D65F10C8596D7E2DAE2633D309B604AE3942E.gpg
@@ -15,3 +15,4 @@
                    because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2013-08-18
 self-signatures SubkeyBinding: 2013-08-18
+third-party GenericCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... voikko-fi-2.5.tar.gz
Signing key on AC5D65F10C8596D7E2DAE2633D309B604AE3942E is not bound:
           No binding signature at time 2022-01-30T10:17:18Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

