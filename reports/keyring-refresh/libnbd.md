# Keyring refresh for libnbd

**Status: still-fails**

Failing call: `--keyring=/builddir/new/libguestfs.keyring --signature=/builddir/new/libnbd-1.25.7.tar.gz.sig --data=/builddir/new/libnbd-1.25.7.tar.gz`

Phase 1 reason: `sha1-cert`

## libguestfs.keyring

- certificates: F7774FB1AD074A7E8C8767EA91738F73E1B768A0, 2B7C1A53420D4AF3BFF4738BF382AE19F4850180, 71C2CC22B1C4602927D2F3AAA7A16B4A2527436A, BC2BFC18CF52DEA925F51215C9A12EDF2527436A
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 82814 → 102583 bytes

```diff
--- dist-git/libguestfs.keyring
+++ refreshed/libguestfs.keyring
@@ -1,15 +1,3 @@
-      Fingerprint: F7774FB1AD074A7E8C8767EA91738F73E1B768A0
-                   Invalid: No binding signature at time 2026-10-12T11:55:41Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: 9076C237217722E17EACCA679658E5232D07308A
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-12T11:55:41Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Richard W.M. Jones <rich@annexia.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Richard W.M. Jones <rjones@redhat.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
       Fingerprint: 2B7C1A53420D4AF3BFF4738BF382AE19F4850180
                    Invalid: No binding signature at time 2026-10-12T11:55:41Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
            Subkey: 94241CEEF03875798D0828FA4B1BA5190E52924D
@@ -37,10 +25,23 @@
            UserID: Eric Blake <eblake@redhat.com>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
+      Fingerprint: F7774FB1AD074A7E8C8767EA91738F73E1B768A0
+                   Invalid: No binding signature at time 2026-10-12T11:55:41Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+           Subkey: 9076C237217722E17EACCA679658E5232D07308A
+                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
+                   Invalid: primary key: No binding signature at time 2026-10-12T11:55:41Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+           UserID: Richard W.M. Jones <rich@annexia.org>
+                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
+           UserID: Richard W.M. Jones <rjones@redhat.com>
+                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
 self-signatures GenericCertification: 2010-04-16, 2011-10-11
 self-signatures KeyRevocation: 2016-08-16
-self-signatures PositiveCertification: 2010-04-16, 2011-10-11, 2014-08-05
-self-signatures SubkeyBinding: 2010-02-22, 2010-04-16, 2011-10-11
+self-signatures PositiveCertification: 2004-12-18, 2010-02-22, 2010-04-16, 2011-10-11, 2014-08-05
+self-signatures SubkeyBinding: 2004-12-18, 2010-02-22, 2010-04-16, 2011-10-11
 third-party CasualCertification: 5
-third-party GenericCertification: 30
-third-party PositiveCertification: 10
+third-party GenericCertification: 36
+third-party PersonaCertification: 1
+third-party PositiveCertification: 11
```

## Verification with the refreshed keyring

```
$ sqv ... libnbd-1.25.7.tar.gz
Signing key on F7774FB1AD074A7E8C8767EA91738F73E1B768A0 is not bound:
           No binding signature at time 2026-07-28T10:57:49Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

