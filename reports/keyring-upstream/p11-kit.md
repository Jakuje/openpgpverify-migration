# Keyring update from upstream for p11-kit

**Status: proposed**

Failing call: `--keyring=/builddir/new/p11-kit-release-keyring.gpg --signature=/builddir/new/p11-kit-0.26.5.tar.xz.sig --data=/builddir/new/p11-kit-0.26.5.tar.xz`

Phase 1 reason: `expired`

## p11-kit-release-keyring.gpg

- from: https://p11-glue.github.io/p11-glue/p11-kit/p11-kit-release-keyring.gpg
- certificates (unchanged): 5D46CB0F763405A7053556F47A75A648B3F9220C, 462225C3B46F34879FC8496CD605848ED7E69871
- size: 11688 → 13085 bytes

```
curl -fsSL -o p11-kit-release-keyring.gpg https://p11-glue.github.io/p11-glue/p11-kit/p11-kit-release-keyring.gpg
```

```diff
--- dist-git/p11-kit-release-keyring.gpg
+++ upstream/p11-kit-release-keyring.gpg
@@ -1,25 +1,22 @@
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
-                   Invalid: No binding signature at time 2026-10-27T11:31:32Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: The primary key is not live: Expired on 2026-06-29T08:24:20Z
+  Expiration time: 2026-06-29 08:24:20 UTC (creation time + 16years 11months 6days 7h 15m 18s)
+        Key flags: certification, signing
            Subkey: 2567E23B4A79AD4DC685099850AD4600C8C530D6
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-27T11:31:32Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-06-29T08:24:20Z
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Daiki Ueno <ueno@gnu.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Daiki Ueno <ueno@unixuser.org>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2009-07-23, 2018-09-26, 2021-12-23
-self-signatures SubkeyBinding: 2010-02-04, 2021-12-23
+self-signatures PositiveCertification: 2009-07-23, 2018-09-26, 2021-12-23, 2023-06-30, 2025-09-18
+self-signatures SubkeyBinding: 2010-02-04, 2023-07-03, 2024-01-02
 third-party GenericCertification: 8
 third-party PositiveCertification: 1
```

## Verification with the upstream keyring

```
$ sqv ... p11-kit-0.26.5.tar.xz
5D46CB0F763405A7053556F47A75A648B3F9220C
rc=0
```

