# Keyring update from upstream for libtpms

**Status: still-fails**

Failing call: `--keyring=/builddir/new/gpgkey-B818B9CADF9089C2D5CEC66B75AD65802A0B4211.asc --signature=/builddir/new/libtpms-0.10.2.tar.gz.asc --data=/builddir/new/libtpms-0.10.2.tar.gz`

Phase 1 reason: `sha1-cert`

## gpgkey-B818B9CADF9089C2D5CEC66B75AD65802A0B4211.asc

- from: https://github.com/stefanberger.gpg
- certificates (unchanged): B818B9CADF9089C2D5CEC66B75AD65802A0B4211
- size: 945 → 944 bytes

```
curl -fsSL -o gpgkey-B818B9CADF9089C2D5CEC66B75AD65802A0B4211.asc https://github.com/stefanberger.gpg
```

```diff
(no change in sq inspect summary)
```

## Verification with the upstream keyring

```
$ sqv ... libtpms-0.10.2.tar.gz
Signing key on B818B9CADF9089C2D5CEC66B75AD65802A0B4211 is not bound:
           No binding signature at time 2026-01-02T16:06:58Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

