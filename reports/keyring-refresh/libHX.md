# Keyring refresh for libHX

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D.gpg --signature=/builddir/new/libHX-3.22.tar.asc --data=-`

Phase 1 reason: `sha1-sig`

## gpgkey-B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D.gpg

- certificates: B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 5659 → 5827 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network search --output - B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D \
  | sq keyring filter --experimental --cert B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D --output update.pgp
sq keyring merge gpgkey-B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D.gpg update.pgp | sq packet dearmor --output gpgkey-B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D.gpg.new
mv gpgkey-B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D.gpg.new gpgkey-B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D.gpg
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

Host verification skipped (data from stdin or a generated file); run phase1.py after approval.

