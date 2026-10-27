# Keyring refresh for fcitx5-zhuyin

**Status: proposed**

Failing call: `--keyring=/builddir/new/0x8E8B898CBF2412F9 --signature=/builddir/new/fcitx5-zhuyin-5.1.9_dict.tar.zst.sig --data=/builddir/new/fcitx5-zhuyin-5.1.9_dict.tar.zst`

Phase 1 reason: `sha1-cert`

## 0x8E8B898CBF2412F9

- certificates: 2CC8A0609AD2A479C65B6D5C8E8B898CBF2412F9
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 7830 → 11093 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network search --output - 2CC8A0609AD2A479C65B6D5C8E8B898CBF2412F9 \
  | sq keyring filter --experimental --cert 2CC8A0609AD2A479C65B6D5C8E8B898CBF2412F9 --output update.pgp
sq keyring merge --output 0x8E8B898CBF2412F9.new 0x8E8B898CBF2412F9 update.pgp
mv 0x8E8B898CBF2412F9.new 0x8E8B898CBF2412F9
```

```diff
--- dist-git/0x8E8B898CBF2412F9
+++ refreshed/0x8E8B898CBF2412F9
@@ -1,15 +1,13 @@
       Fingerprint: 2CC8A0609AD2A479C65B6D5C8E8B898CBF2412F9
-                   Invalid: No binding signature at time 2026-10-27T10:52:01Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: 5D5BB5D0FFB8A3697A5ABFF01D4174D1707CCADF
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-27T10:52:01Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
            UserID: Weng Xuetian <csslayer@chakra-project.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
+                   Revoked:
            UserID: Weng Xuetian <wengxt@gmail.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2010-09-18, 2012-03-17
+self-signatures CertificationRevocation: 2022-04-19, 2022-12-30
+self-signatures PositiveCertification: 2010-09-18, 2012-03-17, 2021-03-26
 self-signatures SubkeyBinding: 2010-09-18
-third-party GenericCertification: 3
+third-party GenericCertification: 4
```

## Verification with the refreshed keyring

```
$ sqv ... fcitx5-zhuyin-5.1.9_dict.tar.zst
2CC8A0609AD2A479C65B6D5C8E8B898CBF2412F9
rc=0
```

