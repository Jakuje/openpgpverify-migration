# Keyring refresh for libguestfs

**Status: still-fails**

Failing call: `--keyring=/builddir/new/libguestfs.keyring --signature=/builddir/new/libguestfs-1.61.4.tar.gz.sig --data=/builddir/new/libguestfs-1.61.4.tar.gz`

Phase 1 reason: `sha1-cert`

## libguestfs.keyring

- certificates: F7774FB1AD074A7E8C8767EA91738F73E1B768A0
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 2823 → 19398 bytes

```diff
--- dist-git/libguestfs.keyring
+++ refreshed/libguestfs.keyring
@@ -12,3 +12,6 @@
                    because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2011-10-11
 self-signatures SubkeyBinding: 2011-10-11
+third-party CasualCertification: 2
+third-party GenericCertification: 6
+third-party PositiveCertification: 2
```

## Verification with the refreshed keyring

```
$ sqv ... libguestfs-1.61.4.tar.gz
Signing key on F7774FB1AD074A7E8C8767EA91738F73E1B768A0 is not bound:
           No binding signature at time 2026-10-02T08:32:54Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

