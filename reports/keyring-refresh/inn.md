# Keyring refresh for inn

**Status: proposed**

Failing call: `--keyring=/builddir/new/0xD73934B49674CF5CCD9AC2787D80315C5736DE75.gpg --signature=/builddir/new/inn-2.7.4.tar.gz.asc --data=/builddir/new/inn-2.7.4.tar.gz`

Phase 1 reason: `expired`

## 0xD73934B49674CF5CCD9AC2787D80315C5736DE75.gpg

- certificates: E784364E8DDE7BB370FBD9EAD15D313882004173
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 6548 → 245097 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network search --output - E784364E8DDE7BB370FBD9EAD15D313882004173 \
  | sq keyring filter --experimental --cert E784364E8DDE7BB370FBD9EAD15D313882004173 --output update.pgp
sq keyring merge 0xD73934B49674CF5CCD9AC2787D80315C5736DE75.gpg update.pgp | sq packet dearmor --output 0xD73934B49674CF5CCD9AC2787D80315C5736DE75.gpg.new
mv 0xD73934B49674CF5CCD9AC2787D80315C5736DE75.gpg.new 0xD73934B49674CF5CCD9AC2787D80315C5736DE75.gpg
```

```diff
--- dist-git/0xD73934B49674CF5CCD9AC2787D80315C5736DE75.gpg
+++ refreshed/0xD73934B49674CF5CCD9AC2787D80315C5736DE75.gpg
@@ -1,23 +1,25 @@
       Fingerprint: E784364E8DDE7BB370FBD9EAD15D313882004173
-                   Invalid: The primary key is not live: Expired on 2023-09-19T05:24:13Z
-  Expiration time: 2023-09-19 05:24:13 UTC (creation time + 14years 3months 21days 7h 21m 47s)
+  Expiration time: 2029-10-05 22:59:08 UTC (creation time + 20years 4months 8days 2h 23m 6s)
         Key flags: certification, signing
            Subkey: D73934B49674CF5CCD9AC2787D80315C5736DE75
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2023-09-19T05:24:13Z
-  Expiration time: 2021-09-19 05:25:18 UTC (creation time + 11years 1day 12h 3m 6s)
+  Expiration time: 2027-10-06 23:00:39 UTC (creation time + 17years 18days 17h 38m 27s)
         Key flags: signing
            Subkey: E374EC5D787B50348D17E57C7CE29A76E9769486
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2023-09-19T05:24:13Z
-  Expiration time: 2023-09-19 05:24:56 UTC (creation time + 14years 3months 21days 7h 4m 30s)
+  Expiration time: 2029-10-05 22:59:48 UTC (creation time + 20years 4months 8days 2h 5m 46s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Russ Allbery <eagle@eyrie.org>
            UserID: Russ Allbery <eagle@windlord.stanford.edu>
                    Revoked:
-                   Invalid: No binding signature at time 2026-10-27T10:55:23Z
            UserID: Russ Allbery <rra@cpan.org>
            UserID: Russ Allbery <rra@cs.stanford.edu>
            UserID: Russ Allbery <rra@debian.org>
+           UserID: Russ Allbery <rra@isc.org>
+           UserID: Russ Allbery <rra@lsst.org>
            UserID: Russ Allbery <rra@stanford.edu>
-self-signatures CertificationRevocation: 2014-08-16
-self-signatures PositiveCertification: 2018-09-18, 2020-09-19
-self-signatures SubkeyBinding: 2020-09-19
+                   Revoked:
+self-signatures CertificationRevocation: 2014-08-16, 2019-09-29
+self-signatures PositiveCertification: 2009-05-29, 2010-09-17, 2011-09-20, 2012-09-16, 2014-08-16, 2014-08-29, 2014-09-18, 2016-09-17, 2016-10-27, 2018-09-18, 2020-01-28, 2020-09-19, 2022-07-16, 2022-09-20, 2024-09-24, 2026-10-06
+self-signatures SubkeyBinding: 2009-05-29, 2010-09-17, 2011-03-18, 2011-09-20, 2012-03-17, 2012-09-16, 2013-03-16, 2013-09-16, 2014-03-16, 2014-09-18, 2015-03-21, 2015-09-18, 2016-03-17, 2016-09-17, 2017-03-18, 2017-09-16, 2018-03-17, 2018-09-18, 2019-03-16, 2019-09-29, 2020-03-29, 2020-09-19, 2021-03-20, 2021-09-19, 2022-03-20, 2022-09-20, 2023-03-25, 2023-10-20, 2024-03-17, 2024-09-24, 2025-03-17, 2025-10-08, 2026-04-17, 2026-10-06
+third-party CasualCertification: 6
+third-party GenericCertification: 48
+third-party PositiveCertification: 6
```

## Verification with the refreshed keyring

```
$ sqv ... inn-2.7.4.tar.gz
E784364E8DDE7BB370FBD9EAD15D313882004173
rc=0
```

