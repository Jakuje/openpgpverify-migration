# Keyring update from upstream for uid_wrapper

**Status: proposed**

Failing call: `--keyring=/builddir/new/uid_wrapper.keyring --signature=/builddir/new/uid_wrapper-1.3.2.tar.gz.asc --data=/builddir/new/uid_wrapper-1.3.2.tar.gz`

Phase 1 reason: `sha1-cert`

## uid_wrapper.keyring

- from: https://cryptomilk.org/0x8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D_asn_cryptomilk_org_gpgkey.asc
- completed from keyservers/WKD, found via: WKD; hkps://keys.openpgp.org; hkps://keyserver.ubuntu.com; hkps://sks.pod01.fleetstreetops.com
- certificates (unchanged): 8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D
- size: 3432 → 20849 bytes

```
curl -fsSL -o key.asc https://cryptomilk.org/0x8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D_asn_cryptomilk_org_gpgkey.asc
sq --home=none network search --output - 8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D \
  | sq keyring filter --experimental --cert 8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D --output update.pgp
sq keyring merge key.asc update.pgp | sq packet dearmor --output uid_wrapper.keyring.new
mv uid_wrapper.keyring.new uid_wrapper.keyring
rm -f key.asc update.pgp
```

```diff
--- dist-git/uid_wrapper.keyring
+++ upstream/uid_wrapper.keyring
@@ -1,17 +1,12 @@
       Fingerprint: 8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D
-                   Invalid: No binding signature at time 2026-11-03T10:00:23Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: 9D04ADDA7B3A38E6F9E74DE1668803FBFBA5A04A
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-03T10:00:23Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Andreas Schneider <asn@cryptomilk.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Andreas Schneider <asn@redhat.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Andreas Schneider <asn@samba.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2013-10-05, 2016-03-31
-self-signatures SubkeyBinding: 2013-10-05
+self-signatures PositiveCertification: 2013-10-05, 2016-03-31, 2019-07-16, 2026-10-28
+self-signatures SubkeyBinding: 2013-10-05, 2026-10-28
+third-party CasualCertification: 2
+third-party GenericCertification: 14
+third-party PositiveCertification: 1
```

## Verification with the upstream keyring

```
$ sqv ... uid_wrapper-1.3.2.tar.gz
8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D
rc=0
```

