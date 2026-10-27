# Keyring update from upstream for john

**Status: still-fails**

Failing call: `--keyring=/builddir/new/gpgkey-297AD21CF86C948081520C1805C027FD4BDC136E.gpg --signature=/builddir/new/john-1.9.0.tar.xz.sign --data=/builddir/new/john-1.9.0.tar.xz`

Phase 1 reason: `sha1-sig`

## gpgkey-297AD21CF86C948081520C1805C027FD4BDC136E.gpg

- from: https://www.openwall.com/signatures/openwall-offline-signatures.asc
- certificates (unchanged): 297AD21CF86C948081520C1805C027FD4BDC136E
- size: 2203 → 4937 bytes

```
curl -fsSL -o gpgkey-297AD21CF86C948081520C1805C027FD4BDC136E.gpg https://www.openwall.com/signatures/openwall-offline-signatures.asc
```

```diff
--- dist-git/gpgkey-297AD21CF86C948081520C1805C027FD4BDC136E.gpg
+++ upstream/gpgkey-297AD21CF86C948081520C1805C027FD4BDC136E.gpg
@@ -9,3 +9,4 @@
                    because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2017-11-18
 self-signatures SubkeyBinding: 2017-11-18
+third-party GenericCertification: 1
```

## Verification with the upstream keyring

```
$ sqv ... john-1.9.0.tar.xz
Signing key on 297AD21CF86C948081520C1805C027FD4BDC136E is not bound:
           No binding signature at time 2019-04-12T18:15:32Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

