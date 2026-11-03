# Keyring refresh for nbdkit

**Status: still-fails**

Failing call: `--keyring=/builddir/new/libguestfs.keyring --signature=/builddir/new/nbdkit-1.49.4.tar.gz.sig --data=/builddir/new/nbdkit-1.49.4.tar.gz`

Phase 1 reason: `sha1-cert`

## libguestfs.keyring

- certificates: F7774FB1AD074A7E8C8767EA91738F73E1B768A0, 2B7C1A53420D4AF3BFF4738BF382AE19F4850180, 71C2CC22B1C4602927D2F3AAA7A16B4A2527436A, BC2BFC18CF52DEA925F51215C9A12EDF2527436A
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 82814 → 102583 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network search --output - F7774FB1AD074A7E8C8767EA91738F73E1B768A0 2B7C1A53420D4AF3BFF4738BF382AE19F4850180 71C2CC22B1C4602927D2F3AAA7A16B4A2527436A BC2BFC18CF52DEA925F51215C9A12EDF2527436A \
  | sq keyring filter --experimental --cert F7774FB1AD074A7E8C8767EA91738F73E1B768A0 --cert 2B7C1A53420D4AF3BFF4738BF382AE19F4850180 --cert 71C2CC22B1C4602927D2F3AAA7A16B4A2527436A --cert BC2BFC18CF52DEA925F51215C9A12EDF2527436A --output update.pgp
sq keyring merge libguestfs.keyring update.pgp | sq packet dearmor --output libguestfs.keyring.new
mv libguestfs.keyring.new libguestfs.keyring
```

```diff
--- dist-git/libguestfs.keyring
+++ refreshed/libguestfs.keyring
@@ -39,8 +39,9 @@
                    because: SHA1 is not considered secure
 self-signatures GenericCertification: 2010-04-16, 2011-10-11
 self-signatures KeyRevocation: 2016-08-16
-self-signatures PositiveCertification: 2010-04-16, 2011-10-11, 2014-08-05
-self-signatures SubkeyBinding: 2010-02-22, 2010-04-16, 2011-10-11
+self-signatures PositiveCertification: 2004-12-18, 2010-02-22, 2010-04-16, 2011-10-11, 2014-08-05
+self-signatures SubkeyBinding: 2004-12-18, 2010-02-22, 2010-04-16, 2011-10-11
 third-party CasualCertification: 5
-third-party GenericCertification: 30
-third-party PositiveCertification: 10
+third-party GenericCertification: 36
+third-party PersonaCertification: 1
+third-party PositiveCertification: 11
```

## Verification with the refreshed keyring

```
$ sqv ... nbdkit-1.49.4.tar.gz
Signing key on F7774FB1AD074A7E8C8767EA91738F73E1B768A0 is not bound:
           No binding signature at time 2026-10-17T09:37:59Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

