# Keyring refresh for hxtools

**Status: still-fails**

Failing call: `--keyring=/builddir/new/gpgkey-B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D.gpg --signature=/builddir/new/hxtools-20150304.tar.asc --data=-`

Phase 1 reason: `sha1-sig`

## gpgkey-B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D.gpg

- certificates: B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 5659 → 8033 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network keyserver search B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D --output gpgkey-B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D.gpg --overwrite
```

```diff
--- dist-git/gpgkey-B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D.gpg
+++ refreshed/gpgkey-B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D.gpg
@@ -17,3 +17,4 @@
                    because: SHA1 is not considered secure
 self-signatures PositiveCertification: 2011-05-09
 self-signatures SubkeyBinding: 2011-05-09
+third-party GenericCertification: 1
```

## Verification with the refreshed keyring

```
$ xzcat hxtools-20150304.tar.xz | sqv ... -
Signing key on B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D is not bound:
           No binding signature at time 2015-03-04T16:27:21Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

