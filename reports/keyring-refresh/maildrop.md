# Keyring refresh for maildrop

**Status: still-fails**

Failing call: `--keyring=/builddir/new/pubkey.maildrop --signature=/builddir/new/maildrop-3.1.0.tar.bz2.sig --data=/builddir/new/maildrop-3.1.0.tar.bz2`

Phase 1 reason: `sha1-cert`

## pubkey.maildrop

- certificates: 316AD59DB04A2CE786F627E46B3A62BE279DBF25
- found via: hkps://keyserver.ubuntu.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 3209 → 7932 bytes

```diff
--- dist-git/pubkey.maildrop
+++ refreshed/pubkey.maildrop
@@ -9,4 +9,4 @@
                    because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2013-08-25
 self-signatures SubkeyBinding: 2013-08-25
-third-party GenericCertification: 1
+third-party GenericCertification: 12
```

## Verification with the refreshed keyring

```
$ sqv ... maildrop-3.1.0.tar.bz2
Signing key on 316AD59DB04A2CE786F627E46B3A62BE279DBF25 is not bound:
           No binding signature at time 2022-12-03T02:07:55Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

