# Keyring update from upstream for psad

**Status: still-fails**

Failing call: `--keyring=/builddir/new/4D6644A9DA036904BDA2CB90E6C9E3350D3E7410.gpg --signature=/builddir/new/psad-2.4.6.tar.bz2.asc --data=/builddir/new/psad-2.4.6.tar.bz2`

Phase 1 reason: `sha1-sig`

## 4D6644A9DA036904BDA2CB90E6C9E3350D3E7410.gpg

- from: https://www.cipherdyne.org/signing_key
- certificates (unchanged): 4D6644A9DA036904BDA2CB90E6C9E3350D3E7410
- size: 1711 → 2433 bytes

```
curl -fsSL -o 4D6644A9DA036904BDA2CB90E6C9E3350D3E7410.gpg https://www.cipherdyne.org/signing_key
```

```diff
(no change in sq inspect summary)
```

## Verification with the upstream keyring

```
$ sqv ... psad-2.4.6.tar.bz2
Signing key on 4D6644A9DA036904BDA2CB90E6C9E3350D3E7410 is not bound:
           No binding signature at time 2018-08-01T01:30:39Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

