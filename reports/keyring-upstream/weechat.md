# Keyring update from upstream for weechat

**Status: proposed**

Failing call: `--keyring=/builddir/new/A9AB5AB778FA5C3522FD0378F82F4B16DEC408F8 --signature=/builddir/new/weechat-4.10.1.tar.xz.asc --data=/builddir/new/weechat-4.10.1.tar.xz`

Phase 1 reason: `sha1-cert`

## A9AB5AB778FA5C3522FD0378F82F4B16DEC408F8

- from: https://keys.openpgp.org/vks/v1/by-fingerprint/A9AB5AB778FA5C3522FD0378F82F4B16DEC408F8
- certificates (unchanged): A9AB5AB778FA5C3522FD0378F82F4B16DEC408F8
- size: 3086 → 5029 bytes

```
curl -fsSL -o A9AB5AB778FA5C3522FD0378F82F4B16DEC408F8 https://keys.openpgp.org/vks/v1/by-fingerprint/A9AB5AB778FA5C3522FD0378F82F4B16DEC408F8
```

```diff
--- dist-git/A9AB5AB778FA5C3522FD0378F82F4B16DEC408F8
+++ upstream/A9AB5AB778FA5C3522FD0378F82F4B16DEC408F8
@@ -1,11 +1,7 @@
       Fingerprint: A9AB5AB778FA5C3522FD0378F82F4B16DEC408F8
-                   Invalid: No binding signature at time 2026-10-27T11:31:45Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: 0040FDC77F9F7350F84E043D0EB86EAD06B322DF
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-27T11:31:45Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: transport encryption, data-at-rest encryption
            UserID: WeeChat (signing key) <webmaster@weechat.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2012-10-20
-self-signatures SubkeyBinding: 2012-10-20
+self-signatures PositiveCertification: 2012-10-20, 2025-01-19
+self-signatures SubkeyBinding: 2012-10-20, 2025-01-19
```

## Verification with the upstream keyring

```
$ sqv ... weechat-4.10.1.tar.xz
A9AB5AB778FA5C3522FD0378F82F4B16DEC408F8
rc=0
```

