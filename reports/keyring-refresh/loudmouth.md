# Keyring refresh for loudmouth

**Status: still-fails**

Failing call: `--keyring=/builddir/new/gpgkey-EACADFF156849BC89653139E3C2900DEACB7FC95.gpg --signature=/builddir/new/loudmouth-1.5.4.tar.bz2.asc --data=/builddir/new/loudmouth-1.5.4.tar.bz2`

Phase 1 reason: `sha1-sig`

## gpgkey-EACADFF156849BC89653139E3C2900DEACB7FC95.gpg

- certificates: EACADFF156849BC89653139E3C2900DEACB7FC95
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 1497 → 3202 bytes

```diff
--- dist-git/gpgkey-EACADFF156849BC89653139E3C2900DEACB7FC95.gpg
+++ refreshed/gpgkey-EACADFF156849BC89653139E3C2900DEACB7FC95.gpg
@@ -13,5 +13,7 @@
            UserID: Mikael BERTHE <mikael.berthe@free.fr>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2012-09-21
-self-signatures SubkeyBinding: 2012-09-21
+self-signatures PositiveCertification: 2008-09-21, 2012-09-21, 2016-09-23, 2019-09-29
+self-signatures SubkeyBinding: 2008-09-21, 2012-09-21, 2016-09-23, 2019-09-29
+third-party CertificationRevocation: 1
+third-party GenericCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... loudmouth-1.5.4.tar.bz2
Signing key on EACADFF156849BC89653139E3C2900DEACB7FC95 is not bound:
           No binding signature at time 2021-01-25T20:22:45Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

