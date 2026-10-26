# Keyring refresh for eggdrop

**Status: still-fails**

Failing call: `--keyring=/builddir/new/E01C240484DE7DBE190FE141E7667DE1D1A39AFF --signature=/builddir/new/eggdrop-1.10.2.tar.gz.asc --data=/builddir/new/eggdrop-1.10.2.tar.gz`

Phase 1 reason: `sha1-cert`

## E01C240484DE7DBE190FE141E7667DE1D1A39AFF

- certificates: E01C240484DE7DBE190FE141E7667DE1D1A39AFF
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 3308 → 3951 bytes

```diff
--- dist-git/E01C240484DE7DBE190FE141E7667DE1D1A39AFF
+++ refreshed/E01C240484DE7DBE190FE141E7667DE1D1A39AFF
@@ -9,3 +9,4 @@
                    because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2016-08-30
 self-signatures SubkeyBinding: 2016-08-30
+third-party GenericCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... eggdrop-1.10.2.tar.gz
Signing key on E01C240484DE7DBE190FE141E7667DE1D1A39AFF is not bound:
           No binding signature at time 2026-09-06T15:13:45Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

