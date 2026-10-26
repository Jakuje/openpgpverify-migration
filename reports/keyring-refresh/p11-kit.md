# Keyring refresh for p11-kit

**Status: proposed**

Failing call: `--keyring=/builddir/new/p11-kit-release-keyring.gpg --signature=/builddir/new/p11-kit-0.26.5.tar.xz.sig --data=/builddir/new/p11-kit-0.26.5.tar.xz`

Phase 1 reason: `expired`

## p11-kit-release-keyring.gpg

- certificates: 5D46CB0F763405A7053556F47A75A648B3F9220C, 462225C3B46F34879FC8496CD605848ED7E69871
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://sks.pod01.fleetstreetops.com
- size: 11688 → 21458 bytes

```diff
--- dist-git/p11-kit-release-keyring.gpg
+++ refreshed/p11-kit-release-keyring.gpg
@@ -1,25 +1,20 @@
       Fingerprint: 5D46CB0F763405A7053556F47A75A648B3F9220C
-                   Invalid: The primary key is not live: Expired on 2023-12-23T11:16:51Z
-  Expiration time: 2023-12-23 11:16:51 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2027-09-18 12:46:25 UTC (creation time + 5years 8months 25days 7h 46s)
         Key flags: certification, signing
            Subkey: DF7B507669E926A2A1F09BBB46CFDAE328F33704
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2023-12-23T11:16:51Z
-  Expiration time: 2023-12-23 11:16:51 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2027-01-01 13:13:03 UTC (creation time + 5years 8days 19h 56m 12s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Zoltan Fridrich <zfridric@redhat.com>
       Fingerprint: 462225C3B46F34879FC8496CD605848ED7E69871
-                   Invalid: No binding signature at time 2026-10-26T20:12:18Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2027-10-17 02:52:01 UTC (creation time + 18years 2months 24days 12h 45m 23s)
+        Key flags: certification, signing
            Subkey: 2567E23B4A79AD4DC685099850AD4600C8C530D6
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-26T20:12:18Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Daiki Ueno <ueno@gnu.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Daiki Ueno <ueno@unixuser.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2009-07-23, 2018-09-26, 2021-12-23
-self-signatures SubkeyBinding: 2010-02-04, 2021-12-23
-third-party GenericCertification: 8
+self-signatures PositiveCertification: 2009-07-23, 2012-12-25, 2013-10-05, 2013-10-06, 2018-09-26, 2021-12-23, 2023-06-30, 2024-01-02, 2025-09-18, 2026-10-17
+self-signatures SubkeyBinding: 2010-02-04, 2021-12-23, 2023-07-03, 2024-01-02
+third-party CasualCertification: 1
+third-party CertificationRevocation: 1
+third-party GenericCertification: 11
 third-party PositiveCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... p11-kit-0.26.5.tar.xz
5D46CB0F763405A7053556F47A75A648B3F9220C
rc=0
```

