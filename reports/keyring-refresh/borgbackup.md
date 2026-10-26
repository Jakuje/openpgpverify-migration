# Keyring refresh for borgbackup

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-6D5B_EF9A_DD20_7580_5747_B70F_9F88_FB52_FAF7_B393.gpg --signature=/builddir/new/borgbackup-1.4.5.tar.gz.asc --data=/builddir/new/borgbackup-1.4.5.tar.gz`

Phase 1 reason: `expired`

## gpgkey-6D5B_EF9A_DD20_7580_5747_B70F_9F88_FB52_FAF7_B393.gpg

- certificates: 6D5BEF9ADD2075805747B70F9F88FB52FAF7B393
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 5745 → 162131 bytes

```diff
--- dist-git/gpgkey-6D5B_EF9A_DD20_7580_5747_B70F_9F88_FB52_FAF7_B393.gpg
+++ refreshed/gpgkey-6D5B_EF9A_DD20_7580_5747_B70F_9F88_FB52_FAF7_B393.gpg
@@ -1,22 +1,25 @@
       Fingerprint: 6D5BEF9ADD2075805747B70F9F88FB52FAF7B393
-                   Invalid: The primary key is not live: Expired on 2019-12-24T00:03:19Z
-  Expiration time: 2019-12-24 00:03:19 UTC (creation time + 9years 11months 27days 22h 38m 26s)
         Key flags: certification, signing
            Subkey: 2F81AFFBAB04E11FE8EE65D4243ACFA951F78E01
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2019-12-24T00:03:19Z
-  Expiration time: 2021-03-01 22:40:33 UTC (creation time + 6years 2months 6days 12h 11m 6s)
+  Expiration time: 2029-02-17 10:05:20 UTC (creation time + 14years 1month 24days 10h 9m 29s)
         Key flags: signing
+           Subkey: 3417BA7D795C88DAB6719915A28818512946B68A
+                   Invalid: The subkey is not live: Expired on 2014-12-26T01:25:06Z
+  Expiration time: 2014-12-26 01:25:06 UTC (creation time + 4years 11months 30days 5h 51m 19s)
+        Key flags: transport encryption, data-at-rest encryption
            Subkey: 42B4A35AC7754DC6EC29AFDB80D1C3A354D9A2EF
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2019-12-24T00:03:19Z
-  Expiration time: 2021-03-01 22:40:33 UTC (creation time + 6years 2months 6days 12h 9m 54s)
+  Expiration time: 2029-02-17 10:05:20 UTC (creation time + 14years 1month 24days 10h 8m 17s)
         Key flags: transport encryption, data-at-rest encryption
+           Subkey: 9FCB53A2E7DA4C088568C3FA90A8763631A6CB60
+                   Invalid: Policy rejected non-revocation signature (PrimaryKeyBinding) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
+                   Invalid: Policy rejected non-revocation signature (PrimaryKeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
            UserID: Thomas Waldmann <thomas.j.waldmann@gmail.com>
            UserID: Thomas Waldmann <tw-public@gmx.de>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Thomas Waldmann <tw@waldmann-edv.de>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Thomas Waldmann <twaldmann@thinkmo.de>
-self-signatures PositiveCertification: 2014-06-01, 2014-08-12
-self-signatures SubkeyBinding: 2019-03-02
+self-signatures PositiveCertification: 2009-12-26, 2014-06-01, 2014-08-12, 2020-01-06, 2021-02-14, 2022-02-15, 2024-02-15
+self-signatures SubkeyBinding: 2009-12-25, 2014-12-25, 2015-12-30, 2017-01-06, 2017-11-22, 2019-03-02, 2021-02-14, 2022-02-15, 2024-02-15, 2026-02-18
+third-party CasualCertification: 15
+third-party GenericCertification: 52
+third-party PositiveCertification: 25
```

## Verification with the refreshed keyring

```
$ sqv ... borgbackup-1.4.5.tar.gz
6D5BEF9ADD2075805747B70F9F88FB52FAF7B393
rc=0
```

