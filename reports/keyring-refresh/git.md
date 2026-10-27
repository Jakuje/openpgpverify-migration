# Keyring refresh for git

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-junio.asc --signature=/builddir/new/git-2.56.0.tar.sign --data=-`

Phase 1 reason: `sha1-cert`

## gpgkey-junio.asc

- certificates: 96E07AF25771955980DAD10020D04E5A713660A7
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 9171 → 68809 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network search --output - 96E07AF25771955980DAD10020D04E5A713660A7 \
  | sq keyring filter --experimental --cert 96E07AF25771955980DAD10020D04E5A713660A7 --output update.pgp
sq keyring merge --output gpgkey-junio.asc.new gpgkey-junio.asc update.pgp
mv gpgkey-junio.asc.new gpgkey-junio.asc
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

Host verification skipped (data from stdin or a generated file); run phase1.py after approval.

