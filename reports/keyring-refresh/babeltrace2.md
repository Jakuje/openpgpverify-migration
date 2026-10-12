# Keyring refresh for babeltrace2

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-7F49314A26E0DE78427680E05F1B2A0789F12B11.gpg --signature=/builddir/new/babeltrace2-2.1.2.tar.bz2.asc --data=/builddir/new/babeltrace2-2.1.2.tar.bz2`

Phase 1 reason: `sha1-cert`

## gpgkey-7F49314A26E0DE78427680E05F1B2A0789F12B11.gpg

- certificates: 7F49314A26E0DE78427680E05F1B2A0789F12B11
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 2908 → 15139 bytes

```diff
--- dist-git/gpgkey-7F49314A26E0DE78427680E05F1B2A0789F12B11.gpg
+++ refreshed/gpgkey-7F49314A26E0DE78427680E05F1B2A0789F12B11.gpg
@@ -1,14 +1,14 @@
       Fingerprint: 7F49314A26E0DE78427680E05F1B2A0789F12B11
-                   Invalid: No binding signature at time 2026-10-12T11:54:56Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2027-06-05 15:41:30 UTC (creation time + 14years 4months 25days 17h 42m 42s)
+        Key flags: certification, signing
            Subkey: 71238FB42DD1DB7F477BC7728531CBEE0802DE0C
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-12T11:54:56Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
            UserID: Jérémie Galarneau <jeremie.galarneau@efficios.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Jérémie Galarneau <jeremie.galarneau@gmail.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2019-01-22
+self-signatures PositiveCertification: 2013-01-08, 2013-10-01, 2016-11-29, 2019-01-22, 2021-02-19, 2022-03-28, 2024-03-28, 2025-04-11, 2026-06-05
 self-signatures SubkeyBinding: 2013-01-08
+third-party CasualCertification: 1
+third-party GenericCertification: 1
+third-party PositiveCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... babeltrace2-2.1.2.tar.bz2
7F49314A26E0DE78427680E05F1B2A0789F12B11
rc=0
```

