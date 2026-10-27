# Keyring update from upstream for ed

**Status: still-fails**

Failing call: `--keyring=/builddir/new/antoniodiazdiaz-keyring-2026.asc --signature=/builddir/new/ed-1.22.6.tar.lz.sig --data=/builddir/new/ed-1.22.6.tar.lz`

Phase 1 reason: `sha1-sig`

## antoniodiazdiaz-keyring-2026.asc

- from: https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x25B62C9821501AA0
- certificates (unchanged): 1E5AEE0B18C0DEB45D64AA0325B62C9821501AA0
- size: 3171 → 3118 bytes

```
curl -fsSL -o antoniodiazdiaz-keyring-2026.asc https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x25B62C9821501AA0
```

```diff
--- dist-git/antoniodiazdiaz-keyring-2026.asc
+++ upstream/antoniodiazdiaz-keyring-2026.asc
@@ -9,4 +9,3 @@
                    because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2026-01-06
 self-signatures SubkeyBinding: 2026-01-06
-third-party GenericCertification: 1
```

## Verification with the upstream keyring

```
$ sqv ... ed-1.22.6.tar.lz
Signing key on 1E5AEE0B18C0DEB45D64AA0325B62C9821501AA0 is not bound:
           No binding signature at time 2026-08-20T15:50:42Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

