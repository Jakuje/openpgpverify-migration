# Keyring update from upstream for dos2unix

**Status: still-fails**

Failing call: `--keyring=/builddir/new/38C1F572B12725BE.asc --signature=/builddir/new/dos2unix-7.5.7.tar.gz.asc --data=/builddir/new/dos2unix-7.5.7.tar.gz`

Phase 1 reason: `sha1-cert`

## 38C1F572B12725BE.asc

- from: https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x38C1F572B12725BE
- certificates (unchanged): F8F1BEA490496A09CCA328CC38C1F572B12725BE
- size: 1709 → 1915 bytes

```
curl -fsSL -o 38C1F572B12725BE.asc https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x38C1F572B12725BE
```

```diff
--- dist-git/38C1F572B12725BE.asc
+++ upstream/38C1F572B12725BE.asc
@@ -9,3 +9,4 @@
                    because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2014-01-01
 self-signatures SubkeyBinding: 2014-01-01
+third-party CasualCertification: 1
```

## Verification with the upstream keyring

```
$ sqv ... dos2unix-7.5.7.tar.gz
Signing key on F8F1BEA490496A09CCA328CC38C1F572B12725BE is not bound:
           No binding signature at time 2026-08-27T20:46:49Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

