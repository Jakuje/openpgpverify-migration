# Keyring update from upstream for coreutils

**Status: proposed**

Failing call: `--keyring=/builddir/new/coreutils-keyring.gpg --signature=/builddir/new/coreutils-9.12.tar.xz.sig --data=/builddir/new/coreutils-9.12.tar.xz`

Phase 1 reason: `None`

## coreutils-keyring.gpg

- from: https://savannah.gnu.org/project/release-gpgkeys.php?group=coreutils&download=1
- certificates (unchanged): 6C37DC12121A5006BC1DB804DF6FD971306037D9
- size: 20290 → 4898 bytes

```
curl -fsSL -o coreutils-keyring.gpg 'https://savannah.gnu.org/project/release-gpgkeys.php?group=coreutils&download=1'
```

```diff
--- dist-git/coreutils-keyring.gpg
+++ upstream/coreutils-keyring.gpg
@@ -1,19 +1,11 @@
       Fingerprint: 6C37DC12121A5006BC1DB804DF6FD971306037D9
-                   Invalid: No binding signature at time 2026-11-16T10:30:13Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: 5B39036B3C18C1DDB9D1FF4DDBF3EE043A2713EB
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-16T10:30:13Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Pádraig Brady <P@draigBrady.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Pádraig Brady <pbrady@redhat.com>
                    Invalid: No binding signature at time 2026-11-16T10:30:13Z
            UserID: Pádraig Brady <pixelbeat@gnu.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
 self-signatures CertificationRevocation: 2016-01-20
-self-signatures PositiveCertification: 2011-09-23
-self-signatures SubkeyBinding: 2011-09-23
-third-party GenericCertification: 2
-third-party PositiveCertification: 7
+self-signatures PositiveCertification: 2026-11-09
+self-signatures SubkeyBinding: 2026-11-09
```

## coreutils-9.12.tar.xz.sig (new release signature)

- from: https://bugzilla.redhat.com/attachment.cgi?id=2163199
- size: 833 → 833 bytes
- SHA512, made 2026-11-09 14:45:30, by `6C37DC12121A5006BC1DB804DF6FD971306037D9`

## Verification with the upstream keyring

```
$ sqv ... coreutils-9.12.tar.xz
6C37DC12121A5006BC1DB804DF6FD971306037D9
rc=0
```

