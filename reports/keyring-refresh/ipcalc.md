# Keyring refresh for ipcalc

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-1F42418905D8206AA754CCDC29EE58B996865171.gpg --signature=/builddir/new/ipcalc-1.1.0.tar.xz.sig --data=/builddir/new/ipcalc-1.1.0.tar.xz`

Phase 1 reason: `sha1-cert`

## gpgkey-1F42418905D8206AA754CCDC29EE58B996865171.gpg

- certificates: 1F42418905D8206AA754CCDC29EE58B996865171
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 58697 → 68975 bytes

```diff
--- dist-git/gpgkey-1F42418905D8206AA754CCDC29EE58B996865171.gpg
+++ refreshed/gpgkey-1F42418905D8206AA754CCDC29EE58B996865171.gpg
@@ -1,29 +1,28 @@
       Fingerprint: 1F42418905D8206AA754CCDC29EE58B996865171
-                   Invalid: No binding signature at time 2026-10-12T11:55:26Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2028-04-29 16:35:00 UTC (creation time + 19years 11months 25days 9h 50m 24s)
+        Key flags: certification, signing
            Subkey: 59FBB55CA7F3A8AB0C503773D81C4887F1679A65
-                   Invalid: primary key: No binding signature at time 2026-10-12T11:55:26Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2028-02-04 05:45:13 UTC (creation time + 9years 11months 27days 21h 50m 24s)
+        Key flags: signing
            Subkey: 1F9ABA5E96A1227366ED49A19B4A51263E13AF91
-                   Invalid: primary key: No binding signature at time 2026-10-12T11:55:26Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2028-02-04 05:45:46 UTC (creation time + 9years 11months 27days 21h 50m 24s)
+        Key flags: transport encryption, data-at-rest encryption
            Subkey: A812CBFDFCDC4D0BE7A093129D5EAAF69013B842
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-12T11:55:26Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
            Subkey: 98637A1E80A2414A9D6A7F6AA6B2AEE71404A91D
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-12T11:55:26Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
            UserID: Nikos Mavrogiannopoulos <n.mavrogiannopoulos@gmail.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Nikos Mavrogiannopoulos <nmav@gnutls.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Nikos Mavrogiannopoulos <nmav@hushmail.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2008-05-04, 2008-09-15, 2013-02-25
+                   Revoked:
+self-signatures CertificationRevocation: 2021-02-13
+self-signatures PositiveCertification: 2008-05-04, 2008-09-15, 2013-02-25, 2020-01-09, 2021-02-13
 self-signatures SubkeyBinding: 2008-05-04, 2018-02-06
-third-party CasualCertification: 6
-third-party GenericCertification: 24
+third-party CasualCertification: 7
+third-party GenericCertification: 29
 third-party PersonaCertification: 1
-third-party PositiveCertification: 9
+third-party PositiveCertification: 10
```

## Verification with the refreshed keyring

```
$ sqv ... ipcalc-1.1.0.tar.xz
1F42418905D8206AA754CCDC29EE58B996865171
rc=0
```

