# Keyring refresh for munin

**Status: still-fails**

Failing call: `--keyring=/builddir/new/gpgkey-910846ADEE4C5D67C19B3E6F0A24C05998BA4133.asc --signature=/builddir/new/munin-2.0.78.tar.gz.asc --data=/builddir/new/munin-2.0.78.tar.gz`

Phase 1 reason: `expired`

## gpgkey-910846ADEE4C5D67C19B3E6F0A24C05998BA4133.asc

- certificates: 910846ADEE4C5D67C19B3E6F0A24C05998BA4133
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 32529 → 59453 bytes

```diff
--- dist-git/gpgkey-910846ADEE4C5D67C19B3E6F0A24C05998BA4133.asc
+++ refreshed/gpgkey-910846ADEE4C5D67C19B3E6F0A24C05998BA4133.asc
@@ -22,10 +22,18 @@
                    Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-05-22T12:01:53Z
   Expiration time: 2017-09-04 20:29:02 UTC (creation time + 11months 30days 3h 50m 24s)
         Key flags: signing
+           Subkey: BE8A72A5EA1F897FDDC0FE368C9072072A248EDB
+                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-05-22T12:01:53Z
+  Expiration time: 2028-07-01 12:43:51 UTC (creation time + 2years 11months 29days 15h 50m 24s)
+        Key flags: signing
            Subkey: CF489AD07F325388EAEBF859840C7ECC82A78504
                    Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-05-22T12:01:53Z
   Expiration time: 2024-08-14 18:51:19 UTC (creation time + 1year 1month 7days 13h 41s)
         Key flags: signing
+           Subkey: 7EB77CB2911D41822C6E86D15D753DD0E6C6275B
+                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-05-22T12:01:53Z
+  Expiration time: 2028-07-01 12:44:13 UTC (creation time + 2years 11months 29days 15h 50m 24s)
+        Key flags: transport encryption, data-at-rest encryption
            Subkey: 067797BF4B6E9DCD1BA832A088C0235EB6E455A7
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
@@ -43,6 +51,10 @@
                    because: SHA1 is not considered secure
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
            UserID: Steve Schnepp <steve.schnepp@gmail.com>
+           UserID: Steve Schnepp <steve.schnepp@munin-monitoring.org>
            UserID: Steve Schnepp <steve.schnepp@pwkf.org>
-self-signatures PositiveCertification: 2012-03-09, 2012-11-24, 2013-08-08, 2021-12-16, 2024-05-16, 2024-05-22
-self-signatures SubkeyBinding: 2012-03-09, 2013-03-19, 2015-03-22, 2016-09-04, 2017-10-20, 2018-11-17, 2019-11-20, 2023-07-08, 2024-05-16, 2024-05-22
+self-signatures PositiveCertification: 2012-03-09, 2012-11-24, 2013-08-08, 2021-12-16, 2024-05-16, 2024-05-22, 2025-07-02
+self-signatures SubkeyBinding: 2012-03-09, 2013-03-19, 2015-03-22, 2016-09-04, 2017-10-20, 2018-11-17, 2019-11-20, 2023-07-08, 2024-05-16, 2024-05-22, 2025-07-02
+third-party CasualCertification: 1
+third-party GenericCertification: 10
+third-party PositiveCertification: 2
```

## Verification with the refreshed keyring

```
$ sqv ... munin-2.0.78.tar.gz
Signing key on 910846ADEE4C5D67C19B3E6F0A24C05998BA4133 is bad:
           The primary key is not live
  because: Expired on 2025-05-22T12:01:53Z
rc=1
```

