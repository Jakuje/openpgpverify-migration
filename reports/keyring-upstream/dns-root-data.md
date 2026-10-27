# Keyring update from upstream for dns-root-data

**Status: still-fails**

Failing call: `--keyring=/builddir/new/registry-admin.key --data=/builddir/new/named.root --signature=/builddir/new/named.root.sig`

Phase 1 reason: `sha1-sig`

## registry-admin.key

- from: https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xf0cb1a326bdf3f3efa3a01fa937bb869e3a238c5
- certificates (unchanged): F0CB1A326BDF3F3EFA3A01FA937BB869E3A238C5
- size: 5563 → 5563 bytes

```
curl -fsSL -o registry-admin.key https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xf0cb1a326bdf3f3efa3a01fa937bb869e3a238c5
```

```diff
(no change in sq inspect summary)
```

## Verification with the upstream keyring

```
$ sqv ... named.root
Signing key on F0CB1A326BDF3F3EFA3A01FA937BB869E3A238C5 is not bound:
           No binding signature at time 2026-01-26T19:01:32Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

