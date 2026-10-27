# Keyring update from upstream for liblxi

**Status: still-fails**

Failing call: `--keyring=/builddir/new/101BAC1C15B216DBE07A3EEA2BDB4A0944FA00B1 --signature=/builddir/new/liblxi-1.22.tar.xz.asc --data=/builddir/new/liblxi-1.22.tar.xz`

Phase 1 reason: `sha1-cert`

## 101BAC1C15B216DBE07A3EEA2BDB4A0944FA00B1

- from: https://keys.openpgp.org/vks/v1/by-fingerprint/101BAC1C15B216DBE07A3EEA2BDB4A0944FA00B1
- certificates (unchanged): 101BAC1C15B216DBE07A3EEA2BDB4A0944FA00B1
- size: 3261 → 3207 bytes

```
curl -fsSL -o 101BAC1C15B216DBE07A3EEA2BDB4A0944FA00B1 https://keys.openpgp.org/vks/v1/by-fingerprint/101BAC1C15B216DBE07A3EEA2BDB4A0944FA00B1
```

```diff
(no change in sq inspect summary)
```

## Verification with the upstream keyring

```
$ sqv ... liblxi-1.22.tar.xz
Signing key on 101BAC1C15B216DBE07A3EEA2BDB4A0944FA00B1 is not bound:
           No binding signature at time 2024-11-08T18:30:19Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

