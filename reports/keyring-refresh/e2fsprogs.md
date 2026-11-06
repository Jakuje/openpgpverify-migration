# Keyring signing key(s) from keyservers for e2fsprogs

**Status: proposed**

Failing call: `--keyring=/builddir/new/tytso-key.asc --signature=/builddir/new/e2fsprogs-1.47.4.tar.sign --data=-`

Phase 1 reason: `unparseable-cert`

## tytso-key.asc

- v3 (PGP 2) keys in the old keyring, unreadable for sqv: 2
- certificates GnuPG reads in the old keyring: 3
- certificates in the new keyring: 3AB057B7E78D945C8C5591FBD36F769BC11804F0
- dropped: 52C344D60D02CD9B07031447ED3A39E393674C40, 44140F903D4FC37F4082381B475FBA0D103D4013
- added: -
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 465237 → 366420 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network keyserver search 3AB057B7E78D945C8C5591FBD36F769BC11804F0 --output tytso-key.asc --overwrite
```

```diff
--- dist-git/tytso-key.asc (as GnuPG reads it)
+++ new/tytso-key.asc
@@ -1,44 +1,24 @@
-      Fingerprint: 52C344D60D02CD9B07031447ED3A39E393674C40
-                   Invalid: Policy rejected asymmetric algorithm: DSA1024 is not considered secure
-           Subkey: 3AF4690ED2AA4262A84008C5213F1DF8DB988C15
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: Policy rejected asymmetric algorithm, because DSA1024 is not considered secure
-           UserID: Theodore Y. Ts'o <tytso@mit.edu>
-      Fingerprint: 44140F903D4FC37F4082381B475FBA0D103D4013
-                   Invalid: No binding signature at time 2026-11-06T09:25:21Z: Policy rejected non-revocation signature (GenericCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: 57437BFAD7E46AB72A7C1168CBCACBC16963CE7A
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-06T09:25:21Z, because Policy rejected non-revocation signature (GenericCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Theodore Ts'o <tytso@valinux.com>
-                   Invalid: Policy rejected non-revocation signature (GenericCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
       Fingerprint: 3AB057B7E78D945C8C5591FBD36F769BC11804F0
         Key flags: certification, signing
            Subkey: 2B69B954DBFE0879288137C9F2F95956950D81A3
-                   Invalid: The subkey is not live: Expired on 2015-10-02T21:08:43Z
-  Expiration time: 2015-10-02 21:08:43 UTC (creation time + 6months 2days 10h 7m 6s)
+  Expiration time: 2027-10-14 23:44:14 UTC (creation time + 12years 6months 14days 12h 42m 37s)
         Key flags: signing
            Subkey: 8A238833A173C1DB60D59CCDF60754F903885799
-                   Invalid: The subkey is not live: Expired on 2015-10-02T21:09:03Z
-  Expiration time: 2015-10-02 21:09:03 UTC (creation time + 6months 2days 10h 4m 32s)
+  Expiration time: 2027-10-14 23:44:32 UTC (creation time + 12years 6months 14days 12h 40m 1s)
         Key flags: transport encryption, data-at-rest encryption
            Subkey: A1F769CA596F15CEDF652653D814B8F32F894C7A
         Key flags: transport encryption, data-at-rest encryption
            Subkey: A933CD6B33B9F4AF1C1144CA06259228B59ED8DF
         Key flags: authentication
            Subkey: C743E9AD1E36FDCCBF4E0EE9465BBB8C3E430766
-                   Invalid: The subkey is not live: Expired on 2015-10-02T21:09:17Z
-  Expiration time: 2015-10-02 21:09:17 UTC (creation time + 6months 2days 6h 40m 6s)
+  Expiration time: 2027-10-14 23:44:32 UTC (creation time + 12years 6months 14days 9h 15m 21s)
         Key flags: authentication
            UserID: Theodore Ts'o <tytso@debian.org>
            UserID: Theodore Ts'o <tytso@google.com>
            UserID: Theodore Ts'o <tytso@mit.edu>
-self-signatures GenericCertification: 1997-08-12, 1999-07-13, 2010-12-02
-self-signatures PositiveCertification: 2003-11-20, 2010-01-14, 2010-12-02, 2015-03-31
-self-signatures SubkeyBinding: 1997-08-12, 1999-07-13, 2010-12-02, 2014-01-29, 2015-07-04
-third-party CasualCertification: 22
-third-party GenericCertification: 170
+self-signatures PositiveCertification: 2010-12-02, 2015-03-31, 2026-04-22
+self-signatures SubkeyBinding: 2010-12-02, 2014-01-29, 2015-03-31, 2015-07-04, 2015-09-16, 2016-01-20, 2016-05-12, 2016-09-19, 2017-06-17, 2017-12-17, 2018-05-24, 2018-11-17, 2019-05-31, 2019-12-16, 2020-05-17, 2021-01-04, 2021-06-23, 2022-03-22, 2023-06-21, 2024-03-24, 2024-12-24, 2025-04-10, 2026-04-22
+third-party CasualCertification: 6
+third-party GenericCertification: 65
 third-party PersonaCertification: 1
-third-party PositiveCertification: 50
+third-party PositiveCertification: 8
```
- **warning: keyring is 366420 bytes**

## Verification with the refreshed keyring

```
$ xzcat e2fsprogs-1.47.4.tar.xz | sqv ... -
3AB057B7E78D945C8C5591FBD36F769BC11804F0
rc=0
```

