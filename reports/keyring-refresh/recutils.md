# Keyring refresh for recutils

**Status: still-fails**

Failing call: `--keyring=/builddir/new/gpgkey-BDFA5717FC1DD35C2C3832A23EF90523B304AF08.gpg --signature=/builddir/new/recutils-1.9.tar.gz.sig --data=/builddir/new/recutils-1.9.tar.gz`

Phase 1 reason: `sha1-cert`

## gpgkey-BDFA5717FC1DD35C2C3832A23EF90523B304AF08.gpg

- certificates: BDFA5717FC1DD35C2C3832A23EF90523B304AF08
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 2209 → 3890 bytes

```diff
--- dist-git/gpgkey-BDFA5717FC1DD35C2C3832A23EF90523B304AF08.gpg
+++ refreshed/gpgkey-BDFA5717FC1DD35C2C3832A23EF90523B304AF08.gpg
@@ -9,3 +9,4 @@
                    because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2013-11-09
 self-signatures SubkeyBinding: 2013-11-09
+third-party GenericCertification: 4
```

## Verification with the refreshed keyring

```
$ sqv ... recutils-1.9.tar.gz
Signing key on BDFA5717FC1DD35C2C3832A23EF90523B304AF08 is not bound:
           No binding signature at time 2022-04-16T17:43:11Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

