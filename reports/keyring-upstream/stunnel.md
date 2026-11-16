# Keyring update from upstream for stunnel

**Status: proposed**

Failing call: `--keyring=/builddir/new/pgp.asc --signature=/builddir/new/stunnel-5.80.tar.gz.asc --data=/builddir/new/stunnel-5.80.tar.gz`

Phase 1 reason: `sha1-cert`

## pgp.asc

- from: https://www.stunnel.org/pgp.asc
- certificates (unchanged): AC915EA30645D9D3D4DAE4FEB1048932DD3AAAA3
- size: 7940 → 14843 bytes

```
curl -fsSL -o pgp.asc https://www.stunnel.org/pgp.asc
```

```diff
--- dist-git/pgp.asc
+++ upstream/pgp.asc
@@ -1,16 +1,13 @@
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
-self-signatures PositiveCertification: 2022-05-10
+self-signatures PositiveCertification: 2015-02-06, 2022-05-10
 self-signatures SubkeyBinding: 2015-02-06
+third-party GenericCertification: 1
```

## Verification with the upstream keyring

```
$ sqv ... stunnel-5.80.tar.gz
AC915EA30645D9D3D4DAE4FEB1048932DD3AAAA3
rc=0
```

