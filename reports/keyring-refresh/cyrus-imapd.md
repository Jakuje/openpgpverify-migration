# Keyring refresh for cyrus-imapd

**Status: still-fails**

Failing call: `--keyring=/builddir/new/elliefm-pub.key --signature=/builddir/new/cyrus-imapd-3.12.4.tar.gz.sig --data=/builddir/new/cyrus-imapd-3.12.4.tar.gz`

Phase 1 reason: `sha1-cert`

## elliefm-pub.key

- certificates: 5B55619A9D7040A9DEE2A2CB554F04FEB36378E0
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 924 → 1343 bytes

```diff
--- dist-git/elliefm-pub.key
+++ refreshed/elliefm-pub.key
@@ -4,3 +4,4 @@
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2015-04-24
+third-party CasualCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... cyrus-imapd-3.12.4.tar.gz
Signing key on 5B55619A9D7040A9DEE2A2CB554F04FEB36378E0 is not bound:
           No binding signature at time 2026-09-09T01:11:32Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

