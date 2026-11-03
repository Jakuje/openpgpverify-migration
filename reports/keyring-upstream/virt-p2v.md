# Keyring update from upstream for virt-p2v

**Status: proposed**

Failing call: `--keyring=/builddir/new/libguestfs.keyring --signature=/builddir/new/virt-p2v-1.42.4.tar.gz.sig --data=/builddir/new/virt-p2v-1.42.4.tar.gz`

Phase 1 reason: `sha1-cert`

## libguestfs.keyring

- from: https://download.libguestfs.org/rich@annexia.org-pubkey.txt
- **renamed to `rich@annexia.org-pubkey.txt`; its `Source` line becomes the URL**
- certificates (unchanged): F7774FB1AD074A7E8C8767EA91738F73E1B768A0
- size: 2823 → 4004 bytes

```
curl -fsSL -O https://download.libguestfs.org/rich@annexia.org-pubkey.txt
```

```diff
--- dist-git/libguestfs.keyring
+++ upstream/libguestfs.keyring
@@ -1,14 +1,9 @@
       Fingerprint: F7774FB1AD074A7E8C8767EA91738F73E1B768A0
-                   Invalid: No binding signature at time 2026-11-03T10:35:58Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: 9076C237217722E17EACCA679658E5232D07308A
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-03T10:35:58Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2041-10-03 12:04:18 UTC (creation time + 29years 11months 22days 21h 50m 25s)
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Richard W.M. Jones <rich@annexia.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Richard W.M. Jones <rjones@redhat.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2011-10-11
 self-signatures SubkeyBinding: 2011-10-11
```

## Verification with the upstream keyring

```
$ sqv ... virt-p2v-1.42.4.tar.gz
F7774FB1AD074A7E8C8767EA91738F73E1B768A0
rc=0
```

