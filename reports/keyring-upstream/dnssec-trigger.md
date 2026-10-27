# Keyring update from upstream for dnssec-trigger

**Status: still-fails**

Failing call: `--keyring=/builddir/new/wouter.asc --signature=/builddir/new/dnssec-trigger-0.17.tar.gz.asc --data=/builddir/new/dnssec-trigger-0.17.tar.gz`

Phase 1 reason: `sha1-sig`

## wouter.asc

- from: https://keys.openpgp.org/vks/v1/by-fingerprint/EDFAA3F2CA4E6EB05681AF8E9F6F1C2D7E045F8D
- certificates (unchanged): EDFAA3F2CA4E6EB05681AF8E9F6F1C2D7E045F8D
- size: 7806 → 9662 bytes

```
curl -fsSL -o wouter.asc https://keys.openpgp.org/vks/v1/by-fingerprint/EDFAA3F2CA4E6EB05681AF8E9F6F1C2D7E045F8D
```

```diff
--- dist-git/wouter.asc
+++ upstream/wouter.asc
@@ -1,11 +1,9 @@
       Fingerprint: EDFAA3F2CA4E6EB05681AF8E9F6F1C2D7E045F8D
-                   Invalid: The primary key is not live: Expired on 2024-12-07T08:44:37Z
-  Expiration time: 2024-12-07 08:44:37 UTC (creation time + 13years 7months 17days 15h 2m 17s)
+  Expiration time: 2028-02-15 11:00:00 UTC (creation time + 16years 9months 26days 2h 10m 28s)
         Key flags: certification, signing, authentication
            Subkey: 1878F7A84324F90A5DE6A479DCBE094E53FC1275
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2024-12-07T08:44:37Z
-  Expiration time: 2024-12-07 08:44:45 UTC (creation time + 13years 7months 17days 15h 2m 25s)
+  Expiration time: 2028-02-15 11:00:00 UTC (creation time + 16years 9months 26days 2h 10m 28s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: W.C.A. Wijngaards <wouter@nlnetlabs.nl>
-self-signatures PositiveCertification: 2011-04-21, 2016-03-21, 2017-08-29, 2019-12-09
-self-signatures SubkeyBinding: 2011-04-21, 2016-03-21, 2017-08-29, 2019-12-09
+self-signatures PositiveCertification: 2011-04-21, 2016-03-21, 2017-08-29, 2019-12-09, 2024-03-07
+self-signatures SubkeyBinding: 2011-04-21, 2016-03-21, 2017-08-29, 2019-12-09, 2024-03-07
```

## Verification with the upstream keyring

```
$ sqv ... dnssec-trigger-0.17.tar.gz
Signing key on EDFAA3F2CA4E6EB05681AF8E9F6F1C2D7E045F8D is not bound:
           No binding signature at time 2018-06-25T09:00:39Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

