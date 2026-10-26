# Keyring refresh for botan3

**Status: still-fails**

Failing call: `--keyring=/builddir/new/pgpkey.txt --signature=/builddir/new/Botan-3.12.0.tar.xz.asc --data=/builddir/new/Botan-3.12.0.tar.xz`

Phase 1 reason: `sha1-cert`

## pgpkey.txt

- certificates: 621DAF6411E1851C4CF9A2E16211EBF1EFBADFBC, 4E60C73551AF2188DF0A5A6278E9804357123B60, 117510149DF418ABD19CB06D9FFD596FAB50F90D
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 9662 → 11258 bytes

```diff
--- dist-git/pgpkey.txt
+++ refreshed/pgpkey.txt
@@ -18,7 +18,7 @@
            UserID: Jack Lloyd (Git Signing Key) <jack@randombit.net>
            UserID: Jack Lloyd (Git Signing Key) <lloyd@randombit.net>
 self-signatures GenericCertification: 2015-10-11, 2016-03-03
-self-signatures PositiveCertification: 2009-08-07, 2015-03-23, 2016-10-25, 2023-03-03, 2023-10-07
+self-signatures PositiveCertification: 2004-10-30, 2009-08-07, 2015-03-23, 2016-03-03, 2016-06-01, 2016-10-22, 2016-10-25, 2018-01-07, 2020-01-16, 2020-03-03, 2023-03-03, 2023-10-07
 self-signatures SubkeyBinding: 2015-03-23
-third-party GenericCertification: 1
+third-party GenericCertification: 2
 third-party PositiveCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... Botan-3.12.0.tar.xz
Signing key on 621DAF6411E1851C4CF9A2E16211EBF1EFBADFBC is not bound:
           No binding signature at time 2026-05-07T01:39:42Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

