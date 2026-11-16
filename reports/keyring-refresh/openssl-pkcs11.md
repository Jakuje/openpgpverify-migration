# Keyring refresh for openssl-pkcs11

**Status: proposed**

Failing call: `--keyring=/builddir/new/libp11.keyring --signature=/builddir/new/libp11-0.4.21.tar.gz.asc --data=/builddir/new/libp11-0.4.21.tar.gz`

Phase 1 reason: `sha1-cert`

## libp11.keyring

- certificates: AC915EA30645D9D3D4DAE4FEB1048932DD3AAAA3
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 14631 → 18417 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network keyserver search AC915EA30645D9D3D4DAE4FEB1048932DD3AAAA3 --output libp11.keyring --overwrite
```

```diff
--- dist-git/libp11.keyring
+++ refreshed/libp11.keyring
@@ -1,17 +1,13 @@
       Fingerprint: AC915EA30645D9D3D4DAE4FEB1048932DD3AAAA3
         Key flags: certification, signing
-           Subkey: 19FFB7E9CA02BF4B6C464AA2970387EEC478CB9A
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
            Subkey: 2BC7E4E67E3CC0C1BEA72F8C2EFC7FF0D416E014
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
+        Key flags: signing
+           Subkey: 19FFB7E9CA02BF4B6C464AA2970387EEC478CB9A
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Michał Trojnara (auxiliary address) <Michal.Trojnara@gmail.com>
            UserID: Michał Trojnara <Michal.Trojnara@mirt.net>
            UserID: Michał Trojnara <Michal.Trojnara@mobi-com.net>
            UserID: Michał Trojnara <Michal.Trojnara@stunnel.org>
 self-signatures PositiveCertification: 2015-02-06, 2022-05-10
 self-signatures SubkeyBinding: 2015-02-06
-third-party GenericCertification: 5
+third-party GenericCertification: 4
```

## Verification with the refreshed keyring

```
$ sqv ... libp11-0.4.21.tar.gz
AC915EA30645D9D3D4DAE4FEB1048932DD3AAAA3
rc=0
```

