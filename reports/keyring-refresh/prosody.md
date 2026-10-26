# Keyring refresh for prosody

**Status: still-fails**

Failing call: `--keyring=/builddir/new/32A9EDDE3609931EB98CEAC315907E8E7BDD6BFE --signature=/builddir/new/prosody-13.0.7.tar.gz.asc --data=/builddir/new/prosody-13.0.7.tar.gz`

Phase 1 reason: `expired`

## 32A9EDDE3609931EB98CEAC315907E8E7BDD6BFE

- certificates: 32A9EDDE3609931EB98CEAC315907E8E7BDD6BFE
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 6441 → 12446 bytes

```diff
--- dist-git/32A9EDDE3609931EB98CEAC315907E8E7BDD6BFE
+++ refreshed/32A9EDDE3609931EB98CEAC315907E8E7BDD6BFE
@@ -9,3 +9,5 @@
            UserID: Matthew Wild <me@matthewwild.co.uk>
 self-signatures PositiveCertification: 2013-07-07, 2015-07-24, 2020-09-10
 self-signatures SubkeyBinding: 2013-07-07, 2015-07-24, 2020-09-10
+third-party CasualCertification: 3
+third-party GenericCertification: 5
```

## Verification with the refreshed keyring

```
$ sqv ... prosody-13.0.7.tar.gz
Signing key on 32A9EDDE3609931EB98CEAC315907E8E7BDD6BFE is bad:
           The primary key is not live
  because: Expired on 2025-09-09T10:18:15Z
rc=1
```

