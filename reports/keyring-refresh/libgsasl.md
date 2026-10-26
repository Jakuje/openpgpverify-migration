# Keyring refresh for libgsasl

**Status: proposed**

Failing call: `--keyring=/builddir/new/54265e8c.txt --signature=/builddir/new/libgsasl-1.10.0.tar.gz.sig --data=/builddir/new/libgsasl-1.10.0.tar.gz`

Phase 1 reason: `binding-after-signature`

## 54265e8c.txt

- certificates: 9AA9BDB11BB1B99A21285A330664A76954265E8C
- found via: hkps://keys.mailvelope.com, hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 80039 → 90563 bytes

```diff
--- dist-git/54265e8c.txt
+++ refreshed/54265e8c.txt
@@ -17,7 +17,7 @@
            UserID: Simon Josefsson <simon@josefsson.org>
            UserID: Simon Josefsson <simon@yubico.com>
 self-signatures PositiveCertification: 2014-06-22, 2014-08-26, 2015-01-15, 2015-08-13, 2016-04-12, 2016-08-11, 2017-01-25, 2017-08-28, 2018-02-26, 2018-08-02, 2019-03-07, 2020-01-01, 2020-01-25, 2020-12-22, 2021-07-21, 2022-03-21, 2022-10-04
-self-signatures SubkeyBinding: 2022-10-04
+self-signatures SubkeyBinding: 2014-06-22, 2014-08-26, 2015-01-15, 2015-08-13, 2016-04-12, 2016-08-11, 2017-01-25, 2017-08-28, 2018-02-26, 2018-08-02, 2019-03-07, 2020-01-01, 2020-01-25, 2020-12-22, 2021-07-21, 2022-03-21, 2022-10-04
 third-party CasualCertification: 5
-third-party GenericCertification: 25
+third-party GenericCertification: 28
 third-party PositiveCertification: 3
```

## Verification with the refreshed keyring

```
$ sqv ... libgsasl-1.10.0.tar.gz
9AA9BDB11BB1B99A21285A330664A76954265E8C
rc=0
```

