# Keyring refresh for rust

**Status: still-fails**

Failing call: `--keyring=/builddir/new/rust-key.gpg.ascii --signature=/builddir/new/rustc-1.99.0-src.tar.xz.asc --data=/builddir/new/rustc-1.99.0-src.tar.xz`

Phase 1 reason: `sha1-cert`

## rust-key.gpg.ascii

- certificates: 108F66205EAEB0AAA8DD5E1C85AB96E6FA1BE5FE
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 5326 → 13372 bytes

```diff
--- dist-git/rust-key.gpg.ascii
+++ refreshed/rust-key.gpg.ascii
@@ -13,3 +13,6 @@
                    because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2013-09-26
 self-signatures SubkeyBinding: 2013-09-26, 2014-12-15
+third-party CasualCertification: 4
+third-party GenericCertification: 9
+third-party PositiveCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... rustc-1.99.0-src.tar.xz
Signing key on 108F66205EAEB0AAA8DD5E1C85AB96E6FA1BE5FE is not bound:
           No binding signature at time 2026-10-01T12:18:39Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

