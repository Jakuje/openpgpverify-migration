# Keyring refresh for ntpsec

**Status: proposed**

Failing call: `--keyring=/builddir/new/ntpsec.gpg.pub.asc --signature=/builddir/new/ntpsec-1.2.6.tar.gz.asc --data=/builddir/new/ntpsec-1.2.6.tar.gz`

Phase 1 reason: `expired`

## ntpsec.gpg.pub.asc

- certificates: DA3FDF774CC70FA64729EC4505D9B371477C7528, E57235D22764129FA4F2F4D17F52608ED0E49D76
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 8501 → 13295 bytes

```diff
--- dist-git/ntpsec.gpg.pub.asc
+++ refreshed/ntpsec.gpg.pub.asc
@@ -3,16 +3,15 @@
         Key flags: certification, signing
            Subkey: F1B3A359ACD57A7BFE493ABFAE3C53420F49D2EF
         Key flags: transport encryption, data-at-rest encryption
+           UserID: NTPsec Contact <contact@ntpsec.org>
            UserID: NTPsec Security Reporting <security@ntpsec.org>
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
+self-signatures PositiveCertification: 2016-04-14, 2017-02-22, 2020-10-06, 2026-07-31
+self-signatures SubkeyBinding: 2016-04-14, 2020-10-06, 2026-07-31
+third-party GenericCertification: 2
```

## Verification with the refreshed keyring

```
$ sqv ... ntpsec-1.2.6.tar.gz
E57235D22764129FA4F2F4D17F52608ED0E49D76
rc=0
```

