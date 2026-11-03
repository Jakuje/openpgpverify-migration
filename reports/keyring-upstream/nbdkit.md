# Keyring update from upstream for nbdkit

**Status: proposed**

Failing call: `--keyring=/builddir/new/libguestfs.keyring --signature=/builddir/new/nbdkit-1.49.4.tar.gz.sig --data=/builddir/new/nbdkit-1.49.4.tar.gz`

Phase 1 reason: `sha1-cert`

## libguestfs.keyring

- from: https://download.libguestfs.org/rich@annexia.org-pubkey.txt
- merged into the existing keyring (the URL has F7774FB1AD074A7E8C8767EA91738F73E1B768A0 only)
- certificates (unchanged): F7774FB1AD074A7E8C8767EA91738F73E1B768A0, 2B7C1A53420D4AF3BFF4738BF382AE19F4850180, 71C2CC22B1C4602927D2F3AAA7A16B4A2527436A, BC2BFC18CF52DEA925F51215C9A12EDF2527436A
- size: 82814 → 83033 bytes

```
curl -fsSL -o key.asc https://download.libguestfs.org/rich@annexia.org-pubkey.txt
sq keyring merge libguestfs.keyring key.asc | sq packet dearmor --output libguestfs.keyring.new
mv libguestfs.keyring.new libguestfs.keyring
rm -f key.asc
```

```diff
--- dist-git/libguestfs.keyring
+++ upstream/libguestfs.keyring
@@ -1,15 +1,10 @@
       Fingerprint: F7774FB1AD074A7E8C8767EA91738F73E1B768A0
-                   Invalid: No binding signature at time 2026-11-03T09:55:48Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: 9076C237217722E17EACCA679658E5232D07308A
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-03T09:55:48Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2041-10-03 12:04:18 UTC (creation time + 29years 11months 22days 21h 50m 25s)
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Richard W.M. Jones <rich@annexia.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Richard W.M. Jones <rjones@redhat.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
       Fingerprint: 2B7C1A53420D4AF3BFF4738BF382AE19F4850180
                    Invalid: No binding signature at time 2026-11-03T09:55:48Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
            Subkey: 6A1D97FB8E2196B71BEE86CCBE9265468B672E01
```

## Verification with the upstream keyring

```
$ sqv ... nbdkit-1.49.4.tar.gz
F7774FB1AD074A7E8C8767EA91738F73E1B768A0
rc=0
```

