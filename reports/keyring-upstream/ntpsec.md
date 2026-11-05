# Keyring update from upstream for ntpsec

**Status: proposed**

Failing call: `--keyring=/builddir/new/ntpsec.gpg.pub.asc --signature=/builddir/new/ntpsec-1.2.6.tar.gz.asc --data=/builddir/new/ntpsec-1.2.6.tar.gz`

Phase 1 reason: `expired`

## ntpsec.gpg.pub.asc

- from: https://ftp.ntpsec.org/pub/releases/ntpsec.gpg.pub.asc
- **adds keys the URL also holds: B48237761A2690222C995F445A22E330161C3978, B09A8CABE180EC664CC511D82A7C3E36CC282DBE** (asked for)
- certificates (unchanged): DA3FDF774CC70FA64729EC4505D9B371477C7528, E57235D22764129FA4F2F4D17F52608ED0E49D76
- size: 8501 → 23219 bytes

```
curl -fsSL -O https://ftp.ntpsec.org/pub/releases/ntpsec.gpg.pub.asc
```

```diff
--- dist-git/ntpsec.gpg.pub.asc
+++ upstream/ntpsec.gpg.pub.asc
@@ -3,16 +3,34 @@
         Key flags: certification, signing
            Subkey: F1B3A359ACD57A7BFE493ABFAE3C53420F49D2EF
         Key flags: transport encryption, data-at-rest encryption
+           UserID: NTPsec Contact <contact@ntpsec.org>
            UserID: NTPsec Security Reporting <security@ntpsec.org>
+      Fingerprint: B48237761A2690222C995F445A22E330161C3978
+                   Invalid: Policy rejected asymmetric algorithm: DSA3072 is not considered secure
+           Subkey: EA43F260ED749264A5201D8B6D4A4A63C5A6BB27
+                   Invalid: primary key: Policy rejected asymmetric algorithm, because DSA3072 is not considered secure
+           UserID: NTPsec Contact <contact@ntpsec.org>
+           UserID: NTPsec Security Reporting <security@ntpsec.org>
+      Fingerprint: B09A8CABE180EC664CC511D82A7C3E36CC282DBE
+                   Revoked:
+                      Message: Revoked by Mark Atwood <mark.atwood@ntpsec.org>
+                   Invalid: No binding signature at time 2026-11-05T09:38:26Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+           Subkey: 9DB7FAFCF3545F14EF77AB765B56609E99556C0E
+                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
+                   Invalid: primary key: No binding signature at time 2026-11-05T09:38:26Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+           UserID: NTPsec Security Reporting <security@ntpsec.org>
+                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
       Fingerprint: E57235D22764129FA4F2F4D17F52608ED0E49D76
-                   Invalid: The primary key is not live: Expired on 2025-10-05T04:11:25Z
-  Expiration time: 2025-10-05 04:11:25 UTC (creation time + 4years 11months 29days 3h 50m 24s)
+  Expiration time: 2028-07-30 04:21:41 UTC (creation time + 7years 9months 23days 7h 7m 52s)
         Key flags: certification, signing
            Subkey: 4068094035426D1F8F8AA800F8FE4D92CC4090B5
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-10-05T04:11:25Z
-  Expiration time: 2025-10-05 04:11:25 UTC (creation time + 4years 11months 29days 3h 50m 24s)
+  Expiration time: 2028-07-30 04:23:52 UTC (creation time + 7years 9months 23days 7h 10m 3s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: NTPsec Security Reporting <security@ntpsec.org>
-self-signatures PositiveCertification: 2016-04-14, 2020-10-06
-self-signatures SubkeyBinding: 2020-10-06
-third-party GenericCertification: 1
+self-signatures GenericCertification: 2016-04-14
+self-signatures KeyRevocation: 2016-04-14
+self-signatures PositiveCertification: 2015-09-29, 2016-04-14, 2017-02-22, 2018-06-08, 2020-10-06, 2026-07-31
+self-signatures SubkeyBinding: 2015-09-29, 2016-04-14, 2018-06-08, 2020-10-06, 2026-07-31
+third-party GenericCertification: 4
```

## Verification with the upstream keyring

```
$ sqv ... ntpsec-1.2.6.tar.gz
E57235D22764129FA4F2F4D17F52608ED0E49D76
rc=0
```

