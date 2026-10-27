# Keyring update from upstream for spamassassin

**Status: still-fails**

Failing call: `--keyring=/builddir/new/KEYS --signature=/builddir/new/Mail-SpamAssassin-rules-4.0.2.r1928015.tgz.asc --data=/builddir/new/Mail-SpamAssassin-rules-4.0.2.r1928015.tgz`

Phase 1 reason: `sha1-cert`

## KEYS

- from: https://www.apache.org/dist/spamassassin/KEYS
- certificates (unchanged): 26C900A46DD40CD5AD24F6D7DEE01987265FA05B, D8099BC79E17D7E49BC21E31FDE52F40F7D39814, 5E541DC959CB8BAC7C78DFDC4056A61A5244EC45
- size: 13211 → 13212 bytes

```
curl -fsSL -o KEYS https://www.apache.org/dist/spamassassin/KEYS
```

```diff
(no change in sq inspect summary)
```

## Verification with the upstream keyring

```
$ sqv ... Mail-SpamAssassin-rules-4.0.2.r1928015.tgz
Signing key on 5E541DC959CB8BAC7C78DFDC4056A61A5244EC45 is not bound:
           primary key
  because: No binding signature at time 2025-08-27T02:54:22Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

