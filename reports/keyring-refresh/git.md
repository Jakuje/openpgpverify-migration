# Keyring refresh for git

**Status: still-fails**

Failing call: `--keyring=/builddir/new/gpgkey-junio.asc --signature=/builddir/new/git-2.56.0.tar.sign --data=-`

Phase 1 reason: `sha1-cert`

## gpgkey-junio.asc

- certificates: 96E07AF25771955980DAD10020D04E5A713660A7
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 9171 → 68869 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network keyserver search 96E07AF25771955980DAD10020D04E5A713660A7 --output gpgkey-junio.asc --overwrite
```

```diff
--- dist-git/gpgkey-junio.asc
+++ refreshed/gpgkey-junio.asc
@@ -22,4 +22,7 @@
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2011-10-01
-self-signatures SubkeyBinding: 2011-10-01, 2020-01-13
+self-signatures SubkeyBinding: 2011-10-01, 2011-10-03, 2014-09-20, 2014-09-21, 2015-09-21, 2017-07-27, 2020-01-13
+third-party CasualCertification: 3
+third-party GenericCertification: 17
+third-party PositiveCertification: 1
```

## Verification with the refreshed keyring

```
$ xzcat git-2.56.0.tar.xz | sqv ... -
Signing key on 96E07AF25771955980DAD10020D04E5A713660A7 is not bound:
           primary key
  because: No binding signature at time 2026-09-28T04:57:02Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

