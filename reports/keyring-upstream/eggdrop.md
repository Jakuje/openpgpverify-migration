# Keyring update from upstream for eggdrop

**Status: still-fails**

Failing call: `--keyring=/builddir/new/E01C240484DE7DBE190FE141E7667DE1D1A39AFF --signature=/builddir/new/eggdrop-1.10.2.tar.gz.asc --data=/builddir/new/eggdrop-1.10.2.tar.gz`

Phase 1 reason: `sha1-cert`

## E01C240484DE7DBE190FE141E7667DE1D1A39AFF

- from: https://keys.openpgp.org/vks/v1/by-fingerprint/E01C240484DE7DBE190FE141E7667DE1D1A39AFF
- certificates (unchanged): E01C240484DE7DBE190FE141E7667DE1D1A39AFF
- size: 3308 → 3243 bytes

```
curl -fsSL -o E01C240484DE7DBE190FE141E7667DE1D1A39AFF https://keys.openpgp.org/vks/v1/by-fingerprint/E01C240484DE7DBE190FE141E7667DE1D1A39AFF
```

```diff
(no change in sq inspect summary)
```

## Verification with the upstream keyring

```
$ sqv ... eggdrop-1.10.2.tar.gz
Signing key on E01C240484DE7DBE190FE141E7667DE1D1A39AFF is not bound:
           No binding signature at time 2026-09-06T15:13:45Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

