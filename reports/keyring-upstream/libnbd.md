# Keyring update from upstream for libnbd

**Status: proposed**

Failing call: `--keyring=/builddir/new/libguestfs.keyring --signature=/builddir/new/libnbd-1.25.8.tar.gz.sig --data=/builddir/new/libnbd-1.25.8.tar.gz`

Phase 1 reason: `sha1-cert`

## libguestfs.keyring

- from: https://download.libguestfs.org/rich@annexia.org-pubkey.txt
- **renamed to `rich@annexia.org-pubkey.txt`; its `Source` line becomes the URL**
- **replaces the keyring: drops 2B7C1A53420D4AF3BFF4738BF382AE19F4850180, 71C2CC22B1C4602927D2F3AAA7A16B4A2527436A, BC2BFC18CF52DEA925F51215C9A12EDF2527436A** (asked for)
- certificates (kept): F7774FB1AD074A7E8C8767EA91738F73E1B768A0
- size: 82814 → 4004 bytes

```
curl -fsSL -O https://download.libguestfs.org/rich@annexia.org-pubkey.txt
```

```diff
--- dist-git/libguestfs.keyring
+++ upstream/libguestfs.keyring
@@ -1,46 +1,9 @@
       Fingerprint: F7774FB1AD074A7E8C8767EA91738F73E1B768A0
-                   Invalid: No binding signature at time 2026-11-03T10:35:57Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: 9076C237217722E17EACCA679658E5232D07308A
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-03T10:35:57Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2041-10-03 12:04:18 UTC (creation time + 29years 11months 22days 21h 50m 25s)
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Richard W.M. Jones <rich@annexia.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Richard W.M. Jones <rjones@redhat.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-      Fingerprint: 2B7C1A53420D4AF3BFF4738BF382AE19F4850180
-                   Invalid: No binding signature at time 2026-11-03T10:35:57Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: 6A1D97FB8E2196B71BEE86CCBE9265468B672E01
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-03T10:35:57Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: 94241CEEF03875798D0828FA4B1BA5190E52924D
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-03T10:35:57Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Eric Blake (free software programmer) <ebb9@byu.net>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Eric Blake <eblake@redhat.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-      Fingerprint: 71C2CC22B1C4602927D2F3AAA7A16B4A2527436A
-        Key flags: certification, signing
-           Subkey: 44418D9D02D69912052A708ED2051C2FD2E4726C
-        Key flags: transport encryption, data-at-rest encryption
-           UserID: Eric Blake (Free Software Programmer) <ebb9@byu.net>
-           UserID: Eric Blake <eblake@redhat.com>
-      Fingerprint: BC2BFC18CF52DEA925F51215C9A12EDF2527436A
-                   Invalid: No binding signature at time 2026-11-03T10:35:57Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Eric Blake <eblake@redhat.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures GenericCertification: 2010-04-16, 2011-10-11
-self-signatures KeyRevocation: 2016-08-16
-self-signatures PositiveCertification: 2010-04-16, 2011-10-11, 2014-08-05
-self-signatures SubkeyBinding: 2010-02-22, 2010-04-16, 2011-10-11
-third-party CasualCertification: 5
-third-party GenericCertification: 30
-third-party PositiveCertification: 10
+self-signatures PositiveCertification: 2011-10-11
+self-signatures SubkeyBinding: 2011-10-11
```

## Verification with the upstream keyring

```
$ sqv ... libnbd-1.25.8.tar.gz
F7774FB1AD074A7E8C8767EA91738F73E1B768A0
rc=0
```

