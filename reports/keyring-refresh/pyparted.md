# Keyring refresh for pyparted

**Status: proposed**

Failing call: `--keyring=/builddir/new/keyring.gpg --signature=/builddir/new/pyparted-3.13.0.tar.gz.asc --data=/builddir/new/pyparted-3.13.0.tar.gz`

Phase 1 reason: `keybox`

## keyring.gpg

- **format: GnuPG keybox, converted to an OpenPGP keyring (sqv does not read keyboxes)**
- certificates: 08F7C8B3C621950C138F766162977BB9C841B965
- found via: hkps://keyserver.ubuntu.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 4556 → 8104 bytes

Commands (run in a copy of dist-git):

```
gpg --homedir "$(mktemp -d)" --batch --no-default-keyring --keyring ./keyring.gpg --export --output keyring.gpg.pgp
sq --home=none network search --output - 08F7C8B3C621950C138F766162977BB9C841B965 \
  | sq keyring filter --experimental --cert 08F7C8B3C621950C138F766162977BB9C841B965 --output update.pgp
sq keyring merge keyring.gpg.pgp update.pgp | sq packet dearmor --output keyring.gpg.new
mv keyring.gpg.new keyring.gpg
```

```diff
--- dist-git/keyring.gpg (exported from keybox)
+++ refreshed/keyring.gpg
@@ -8,3 +8,4 @@
            UserID: David Lawrence Cantrell, Jr. <dcantrell@redhat.com>
 self-signatures PositiveCertification: 2019-10-14
 self-signatures SubkeyBinding: 2019-10-14
+third-party GenericCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... pyparted-3.13.0.tar.gz
08F7C8B3C621950C138F766162977BB9C841B965
rc=0
```

