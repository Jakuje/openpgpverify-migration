# Keyring refresh for spamassassin

**Status: still-fails**

Failing call: `--keyring=/builddir/new/KEYS --signature=/builddir/new/Mail-SpamAssassin-rules-4.0.2.r1928015.tgz.asc --data=/builddir/new/Mail-SpamAssassin-rules-4.0.2.r1928015.tgz`

Phase 1 reason: `sha1-cert`

## KEYS

- certificates: 26C900A46DD40CD5AD24F6D7DEE01987265FA05B, D8099BC79E17D7E49BC21E31FDE52F40F7D39814, 5E541DC959CB8BAC7C78DFDC4056A61A5244EC45
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 13211 → 11959 bytes

```diff
--- dist-git/KEYS
+++ refreshed/KEYS
@@ -26,8 +26,9 @@
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
 self-signatures CertificationRevocation: 2004-08-16
-self-signatures GenericCertification: 2009-12-02
+self-signatures GenericCertification: 2008-08-07, 2009-12-02, 2010-01-16
 self-signatures PositiveCertification: 2003-06-09, 2003-08-21, 2005-12-20, 2009-12-02
 self-signatures SubkeyBinding: 2003-08-21, 2005-12-20, 2008-01-10, 2009-12-02
-third-party GenericCertification: 2
-third-party PositiveCertification: 4
+third-party CasualCertification: 5
+third-party GenericCertification: 9
+third-party PositiveCertification: 8
```

## Verification with the refreshed keyring

```
$ sqv ... Mail-SpamAssassin-rules-4.0.2.r1928015.tgz
Signing key on 5E541DC959CB8BAC7C78DFDC4056A61A5244EC45 is not bound:
           primary key
  because: No binding signature at time 2025-08-27T02:54:22Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

