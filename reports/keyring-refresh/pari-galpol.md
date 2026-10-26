# Keyring refresh for pari-galpol

**Status: still-fails**

Failing call: `--keyring=/builddir/new/gpgkey-42028EA404A2E9D80AC453148F0E7C2B4522E387.gpg --signature=/builddir/new/galpol.tgz.asc --data=/builddir/new/galpol.tgz`

Phase 1 reason: `sha1-cert`

## gpgkey-42028EA404A2E9D80AC453148F0E7C2B4522E387.gpg

- certificates: 42028EA404A2E9D80AC453148F0E7C2B4522E387
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD
- size: 3458 → 46939 bytes

```diff
--- dist-git/gpgkey-42028EA404A2E9D80AC453148F0E7C2B4522E387.gpg
+++ refreshed/gpgkey-42028EA404A2E9D80AC453148F0E7C2B4522E387.gpg
@@ -1,17 +1,12 @@
       Fingerprint: 42028EA404A2E9D80AC453148F0E7C2B4522E387
-                   Invalid: No binding signature at time 2026-10-26T17:53:55Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: 93896CD39004CCF6FFDA159BAFAFFEDA466708CB
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-26T17:53:55Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Bill Allombert <Bill.Allombert@math.u-bordeaux.fr>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Bill Allombert <Bill.Allombert@math.u-bordeaux1.fr>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Bill Allombert <ballombe@debian.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2012-11-21, 2018-01-27
-self-signatures SubkeyBinding: 2012-11-21
+self-signatures PositiveCertification: 2012-11-21, 2018-01-27, 2026-10-10
+self-signatures SubkeyBinding: 2012-11-21, 2026-10-10
+third-party CasualCertification: 1
+third-party GenericCertification: 23
+third-party PositiveCertification: 3
```

## Verification with the refreshed keyring

```
$ sqv ... galpol.tgz
Signing key on 42028EA404A2E9D80AC453148F0E7C2B4522E387 is not bound:
           No binding signature at time 2018-06-25T13:27:35Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

