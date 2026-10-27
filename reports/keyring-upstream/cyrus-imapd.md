# Keyring update from upstream for cyrus-imapd

**Status: still-fails**

Failing call: `--keyring=/builddir/new/elliefm-pub.key --signature=/builddir/new/cyrus-imapd-3.12.4.tar.gz.sig --data=/builddir/new/cyrus-imapd-3.12.4.tar.gz`

Phase 1 reason: `sha1-cert`

## elliefm-pub.key

- from: https://github.com/elliefm.gpg
- certificates (unchanged): 5B55619A9D7040A9DEE2A2CB554F04FEB36378E0
- size: 924 → 923 bytes

```
curl -fsSL -o elliefm-pub.key https://github.com/elliefm.gpg
```

```diff
(no change in sq inspect summary)
```

## Verification with the upstream keyring

```
$ sqv ... cyrus-imapd-3.12.4.tar.gz
Signing key on 5B55619A9D7040A9DEE2A2CB554F04FEB36378E0 is not bound:
           No binding signature at time 2026-09-09T01:11:32Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

