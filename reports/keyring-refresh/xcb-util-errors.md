# Keyring refresh for xcb-util-errors

**Status: still-fails**

Failing call: `--keyring=/builddir/new/gpgkey-A2FB9E081F2D130E.gpg --signature=/builddir/new/xcb-util-errors-1.0.1.tar.xz.sig --data=/builddir/new/xcb-util-errors-1.0.1.tar.xz`

Phase 1 reason: `binding-after-signature`

## gpgkey-A2FB9E081F2D130E.gpg

- certificates: 4A193C06D35E7C670FA4EF0BA2FB9E081F2D130E
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 3768 → 11349 bytes

```diff
--- dist-git/gpgkey-A2FB9E081F2D130E.gpg
+++ refreshed/gpgkey-A2FB9E081F2D130E.gpg
@@ -9,5 +9,7 @@
            UserID: Alan Coopersmith <alan.coopersmith@oracle.com>
            UserID: Alan Coopersmith <alan.coopersmith@sun.com>
            UserID: Alan Coopersmith <alanc@freedesktop.org>
-self-signatures PositiveCertification: 2023-04-21
-self-signatures SubkeyBinding: 2007-07-16, 2023-04-21
+self-signatures PositiveCertification: 2007-07-16, 2012-03-20, 2013-04-26, 2018-04-22, 2023-04-21
+self-signatures SubkeyBinding: 2007-07-16, 2013-04-26, 2018-04-22, 2023-04-21
+third-party CasualCertification: 1
+third-party GenericCertification: 3
```

## Verification with the refreshed keyring

```
$ sqv ... xcb-util-errors-1.0.1.tar.xz
Signing key on 4A193C06D35E7C670FA4EF0BA2FB9E081F2D130E is not bound:
           primary key
  because: Policy rejected asymmetric algorithm
  because: DSA1024 is not considered secure
rc=1
```

