# Keyring refresh for qemu

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-CEACC9E15534EBABB82D3FA03353C9CEF108B584.gpg --signature=/builddir/new/qemu-11.1.2.tar.xz.sig --data=/builddir/new/qemu-11.1.2.tar.xz`

Phase 1 reason: `sha1-cert`

## gpgkey-CEACC9E15534EBABB82D3FA03353C9CEF108B584.gpg

- certificates: CEACC9E15534EBABB82D3FA03353C9CEF108B584
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 1890 → 27413 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network search --output - CEACC9E15534EBABB82D3FA03353C9CEF108B584 \
  | sq keyring filter --experimental --cert CEACC9E15534EBABB82D3FA03353C9CEF108B584 --output update.pgp
sq keyring merge gpgkey-CEACC9E15534EBABB82D3FA03353C9CEF108B584.gpg update.pgp | sq packet dearmor --output gpgkey-CEACC9E15534EBABB82D3FA03353C9CEF108B584.gpg.new
mv gpgkey-CEACC9E15534EBABB82D3FA03353C9CEF108B584.gpg.new gpgkey-CEACC9E15534EBABB82D3FA03353C9CEF108B584.gpg
```

```diff
--- dist-git/gpgkey-CEACC9E15534EBABB82D3FA03353C9CEF108B584.gpg
+++ refreshed/gpgkey-CEACC9E15534EBABB82D3FA03353C9CEF108B584.gpg
@@ -1,17 +1,21 @@
       Fingerprint: CEACC9E15534EBABB82D3FA03353C9CEF108B584
-                   Invalid: No binding signature at time 2026-10-27T11:04:25Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2031-05-26 21:02:33 UTC (creation time + 17years 7months 6days 22h 58m 2s)
+        Key flags: certification, signing
            Subkey: B771E2672C6A23D7CC3CD7643B0B7D75D7AC684E
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-27T11:04:25Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
            UserID: Michael Roth <flukshun@gmail.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Michael Roth <mdroth@linux.vnet.ibm.com>
+                   Revoked:
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
            UserID: Michael Roth <mdroth@utexas.edu>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2013-10-18
+           UserID: Michael Roth <michael.roth@amd.com>
+self-signatures CertificationRevocation: 2020-10-27
+self-signatures PositiveCertification: 2013-10-18, 2020-10-27, 2024-05-11, 2026-05-27
 self-signatures SubkeyBinding: 2013-10-18
+third-party CasualCertification: 2
+third-party GenericCertification: 8
+third-party PersonaCertification: 2
+third-party PositiveCertification: 2
```

## Verification with the refreshed keyring

```
$ sqv ... qemu-11.1.2.tar.xz
CEACC9E15534EBABB82D3FA03353C9CEF108B584
rc=0
```

