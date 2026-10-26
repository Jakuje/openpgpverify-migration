# Keyring refresh for par2cmdline

**Status: still-fails**

Failing call: `--keyring=/builddir/new/gpg-db2277bcd500aa3825610bdddb323392796ca067.asc --signature=/builddir/new/par2cmdline-1.3.0.tar.bz2.sig --data=/builddir/new/par2cmdline-1.3.0.tar.bz2`

Phase 1 reason: `sha1-cert`

## gpg-db2277bcd500aa3825610bdddb323392796ca067.asc

- certificates: DB2277BCD500AA3825610BDDDB323392796CA067
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 5513 → 8745 bytes

```diff
--- dist-git/gpg-db2277bcd500aa3825610bdddb323392796ca067.asc
+++ refreshed/gpg-db2277bcd500aa3825610bdddb323392796ca067.asc
@@ -9,4 +9,4 @@
                    because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2011-11-03
 self-signatures SubkeyBinding: 2011-11-03
-third-party GenericCertification: 4
+third-party GenericCertification: 9
```

## Verification with the refreshed keyring

```
$ sqv ... par2cmdline-1.3.0.tar.bz2
Signing key on DB2277BCD500AA3825610BDDDB323392796CA067 is not bound:
           No binding signature at time 2026-08-15T08:09:31Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

