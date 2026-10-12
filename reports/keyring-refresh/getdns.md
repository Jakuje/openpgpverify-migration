# Keyring refresh for getdns

**Status: still-fails**

Failing call: `--keyring=/builddir/new/willem.nlnetlabs.nl --signature=/builddir/new/getdns-1.7.3.tar.gz.asc --data=/builddir/new/getdns-1.7.3.tar.gz`

Phase 1 reason: `sha1-cert`

## willem.nlnetlabs.nl

- certificates: DC34EE5DB2417BCC151E5100E5F8F8212F77A498
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 20484 → 15872 bytes

```diff
--- dist-git/willem.nlnetlabs.nl
+++ refreshed/willem.nlnetlabs.nl
@@ -7,8 +7,8 @@
            UserID: Willem Toorop <willem@nlnetlabs.nl>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2011-03-01, 2016-02-29
-self-signatures SubkeyBinding: 2011-03-01, 2016-02-29
+self-signatures PositiveCertification: 2011-03-01, 2016-02-29, 2019-12-30
+self-signatures SubkeyBinding: 2011-03-01, 2016-02-29, 2019-12-30
 third-party CasualCertification: 1
 third-party GenericCertification: 22
 third-party PositiveCertification: 6
```

## Verification with the refreshed keyring

```
$ sqv ... getdns-1.7.3.tar.gz
Signing key on DC34EE5DB2417BCC151E5100E5F8F8212F77A498 is not bound:
           No binding signature at time 2022-12-22T14:34:22Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

