# Keyring refresh for paperkey

**Status: still-fails**

Failing call: `--keyring=/builddir/new/gpgkey-DB698D7199242560.asc --signature=/builddir/new/paperkey-1.6.tar.gz.sig --data=/builddir/new/paperkey-1.6.tar.gz`

Phase 1 reason: `sha1-cert`

## gpgkey-DB698D7199242560.asc

- certificates: 7D92FD313AB6F3734CC59CA1DB698D7199242560
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 4239 → 51125 bytes

```diff
--- dist-git/gpgkey-DB698D7199242560.asc
+++ refreshed/gpgkey-DB698D7199242560.asc
@@ -1,15 +1,25 @@
       Fingerprint: 7D92FD313AB6F3734CC59CA1DB698D7199242560
                    Invalid: No binding signature at time 2026-10-26T17:51:46Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
            Subkey: 74C76C2E15E77BDE974D17985B47A9CC6F410A43
+                   Invalid: primary key: No binding signature at time 2026-10-26T17:51:46Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+           Subkey: A1543829812C9EA987F14526FEA78A7AA1BC4FA4
+                   Invalid: Policy rejected non-revocation signature (PrimaryKeyBinding) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
+                   Invalid: primary key: No binding signature at time 2026-10-26T17:51:46Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+           Subkey: F0EC51D92ED0C1838977DDD0AE2827D11643B926
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
                    Invalid: primary key: No binding signature at time 2026-10-26T17:51:46Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: A1543829812C9EA987F14526FEA78A7AA1BC4FA4
+           Subkey: FC2A0E9B51227D7B59232CE6E2665C8749E1CBC9
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
                    Invalid: primary key: No binding signature at time 2026-10-26T17:51:46Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
            UserID: David M. Shaw <dshaw@jabberwocky.com>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2012-01-10
-self-signatures SubkeyBinding: 2017-02-12
+self-signatures PositiveCertification: 2002-01-28, 2012-01-10
+self-signatures SubkeyBinding: 2002-01-28, 2006-03-11, 2012-01-10, 2017-02-12, 2023-09-26
+third-party CasualCertification: 12
+third-party GenericCertification: 83
+third-party PersonaCertification: 3
+third-party PositiveCertification: 25
```

## Verification with the refreshed keyring

```
$ sqv ... paperkey-1.6.tar.gz
Signing key on 7D92FD313AB6F3734CC59CA1DB698D7199242560 is not bound:
           primary key
  because: No binding signature at time 2018-10-19T13:47:19Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

