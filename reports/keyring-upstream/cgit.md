# Keyring update from upstream for cgit

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-AB9942E6D4A4CFC3412620A749FC7012A5DE03AE.asc --signature=/builddir/new/cgit-1.3.tar.asc --data=-`

Phase 1 reason: `expired`

## gpgkey-AB9942E6D4A4CFC3412620A749FC7012A5DE03AE.asc

- from: https://www.zx2c4.com/keys/AB9942E6D4A4CFC3412620A749FC7012A5DE03AE.asc
- certificates (unchanged): AB9942E6D4A4CFC3412620A749FC7012A5DE03AE
- size: 28765 → 3155 bytes

```
curl -fsSL -o gpgkey-AB9942E6D4A4CFC3412620A749FC7012A5DE03AE.asc https://www.zx2c4.com/keys/AB9942E6D4A4CFC3412620A749FC7012A5DE03AE.asc
```

```diff
--- dist-git/gpgkey-AB9942E6D4A4CFC3412620A749FC7012A5DE03AE.asc
+++ upstream/gpgkey-AB9942E6D4A4CFC3412620A749FC7012A5DE03AE.asc
@@ -1,14 +1,9 @@
       Fingerprint: AB9942E6D4A4CFC3412620A749FC7012A5DE03AE
-                   Invalid: The primary key is not live: Expired on 2022-02-11T13:41:11Z
-  Expiration time: 2022-02-11 13:41:11 UTC (creation time + 11years 26days 20h 58m 15s)
+  Expiration time: 2027-03-31 19:17:27 UTC (creation time + 16years 2months 13days 23h 27m 19s)
         Key flags: certification, signing
            Subkey: 472A073D982F00805C932395D4F7A95DFB1EFB7F
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-02-11T13:41:11Z
-  Expiration time: 2022-02-11 13:41:39 UTC (creation time + 11years 26days 20h 58m 43s)
+  Expiration time: 2027-03-31 19:17:36 UTC (creation time + 16years 2months 13days 23h 27m 28s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Jason A. Donenfeld <Jason@zx2c4.com>
-self-signatures PositiveCertification: 2011-01-15, 2013-03-29, 2013-10-31, 2014-11-07, 2015-03-18, 2017-02-10, 2021-02-11
-self-signatures SubkeyBinding: 2021-02-11
-third-party CasualCertification: 1
-third-party GenericCertification: 19
-third-party PositiveCertification: 7
+self-signatures PositiveCertification: 2024-03-31
+self-signatures SubkeyBinding: 2024-03-31
```

Host verification skipped (data from stdin or a generated file); run phase1.py after approval.

