# Keyring refresh for i3lock

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-424E14D703E7C6D43D9D6F364E7160ED4AC8EE1D.gpg --signature=/builddir/new/i3lock-2.16.tar.xz.asc --data=/builddir/new/i3lock-2.16.tar.xz`

Phase 1 reason: `expired`

## gpgkey-424E14D703E7C6D43D9D6F364E7160ED4AC8EE1D.gpg

- certificates: 424E14D703E7C6D43D9D6F364E7160ED4AC8EE1D
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 2475 → 226516 bytes

```diff
--- dist-git/gpgkey-424E14D703E7C6D43D9D6F364E7160ED4AC8EE1D.gpg
+++ refreshed/gpgkey-424E14D703E7C6D43D9D6F364E7160ED4AC8EE1D.gpg
@@ -1,8 +1,10 @@
       Fingerprint: 424E14D703E7C6D43D9D6F364E7160ED4AC8EE1D
-                   Invalid: The primary key is not live: Expired on 2022-05-05T11:36:21Z
-  Expiration time: 2022-05-05 11:36:21 UTC (creation time + 12years 11months 14days 6h 11m 58s)
+  Expiration time: 2030-01-21 19:42:26 UTC (creation time + 20years 8months 1day 21h 58m 51s)
         Key flags: certification, signing, authentication, transport encryption, data-at-rest encryption
            UserID: Michael Stapelberg (RENT-A-GURU) <michael@rent-a-guru.de>
            UserID: Michael Stapelberg <michael@stapelberg.de>
            UserID: Michael Stapelberg <stapelberg@debian.org>
-self-signatures PositiveCertification: 2017-05-06
+self-signatures PositiveCertification: 2009-05-21, 2012-03-28, 2014-04-27, 2017-05-06, 2020-05-21, 2025-01-22
+third-party CasualCertification: 19
+third-party GenericCertification: 85
+third-party PositiveCertification: 20
```

## Verification with the refreshed keyring

```
$ sqv ... i3lock-2.16.tar.xz
424E14D703E7C6D43D9D6F364E7160ED4AC8EE1D
rc=0
```

