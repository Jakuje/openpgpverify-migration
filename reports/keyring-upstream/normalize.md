# Keyring update from upstream for normalize

**Status: still-fails**

Failing call: `--keyring=/builddir/new/0xAFC8519A83FE7486.gpg --signature=/builddir/new/normalize-0.7.7.tar.gz.sig --data=/builddir/new/normalize-0.7.7.tar.gz`

Phase 1 reason: `v3-sig`

## 0xAFC8519A83FE7486.gpg

- from: https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x659d42b60f3b86ea4d37777eafc8519a83fe7486
- certificates (unchanged): 659D42B60F3B86EA4D37777EAFC8519A83FE7486
- size: 839 → 1708 bytes

```
curl -fsSL -o 0xAFC8519A83FE7486.gpg https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x659d42b60f3b86ea4d37777eafc8519a83fe7486
```

```diff
--- dist-git/0xAFC8519A83FE7486.gpg
+++ upstream/0xAFC8519A83FE7486.gpg
@@ -1,6 +1,11 @@
       Fingerprint: 659D42B60F3B86EA4D37777EAFC8519A83FE7486
                    Invalid: No binding signature at time 2026-10-27T11:31:29Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+           Subkey: DBC4EFC700C7D1A328F141C30EA962283B9762BB
+                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
+                   Invalid: primary key: No binding signature at time 2026-10-27T11:31:29Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
            UserID: Chris Vaill <chrisvaill@gmail.com>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2005-07-13
+self-signatures SubkeyBinding: 2005-07-13
```

## Verification with the upstream keyring

```
$ sqv ... normalize-0.7.7.tar.gz
Error: Policy rejected packet type

Caused by:
    Signature Packet v3 is not considered secure since 2021-02-01T00:00:00Z
rc=1
```

