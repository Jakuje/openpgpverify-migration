# Keyring refresh for asterisk

**Status: proposed**

Failing call: `--keyring=/builddir/new/asterisk-gpgkeys.gpg --signature=/builddir/new/asterisk-23.5.0.tar.gz.asc --data=/builddir/new/asterisk-23.5.0.tar.gz`

Phase 1 reason: `keybox`

## asterisk-gpgkeys.gpg

- **format: GnuPG keybox, converted to an OpenPGP keyring (sqv does not read keyboxes)**
- certificates: F2FC93DB7587BD1FB49E045A5D984BE337191CE7, 0F77FB5D216A02390B4C51DB7C2C8A8BCB3F61BD, 57E769BC37906C091E7F641F6CB44E557BD982D8, 551F29104B2106080C6C2851073B0C1FC9B2E352, 639D932D5170532F8C200CCD9C59F000777DCC45, CDBEE4CC699E200EB4D46BB79E76E3A42341CE04, 80CEBC345EC9FF529B4B7B808438CBA18D0CAA72, 21A91EB1F012252993E9BF4A368AB332B59975F3
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 23332 → 41901 bytes

Commands (run in a copy of dist-git):

```
gpg --homedir "$(mktemp -d)" --batch --no-default-keyring --keyring ./asterisk-gpgkeys.gpg --export --output asterisk-gpgkeys.gpg.pgp
sq --home=none network search --output - F2FC93DB7587BD1FB49E045A5D984BE337191CE7 0F77FB5D216A02390B4C51DB7C2C8A8BCB3F61BD 57E769BC37906C091E7F641F6CB44E557BD982D8 551F29104B2106080C6C2851073B0C1FC9B2E352 639D932D5170532F8C200CCD9C59F000777DCC45 CDBEE4CC699E200EB4D46BB79E76E3A42341CE04 80CEBC345EC9FF529B4B7B808438CBA18D0CAA72 21A91EB1F012252993E9BF4A368AB332B59975F3 \
  | sq keyring filter --experimental --cert F2FC93DB7587BD1FB49E045A5D984BE337191CE7 --cert 0F77FB5D216A02390B4C51DB7C2C8A8BCB3F61BD --cert 57E769BC37906C091E7F641F6CB44E557BD982D8 --cert 551F29104B2106080C6C2851073B0C1FC9B2E352 --cert 639D932D5170532F8C200CCD9C59F000777DCC45 --cert CDBEE4CC699E200EB4D46BB79E76E3A42341CE04 --cert 80CEBC345EC9FF529B4B7B808438CBA18D0CAA72 --cert 21A91EB1F012252993E9BF4A368AB332B59975F3 --output update.pgp
sq keyring merge asterisk-gpgkeys.gpg.pgp update.pgp | sq packet dearmor --output asterisk-gpgkeys.gpg.new
mv asterisk-gpgkeys.gpg.new asterisk-gpgkeys.gpg
```

```diff
--- dist-git/asterisk-gpgkeys.gpg (exported from keybox)
+++ refreshed/asterisk-gpgkeys.gpg
@@ -61,13 +61,16 @@
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
       Fingerprint: 21A91EB1F012252993E9BF4A368AB332B59975F3
-                   Invalid: No binding signature at time 2026-10-27T10:49:55Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: 993583DE8CB2CEB44ACDE5EBEE5B5FF60C3CF379
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-27T10:49:55Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
            UserID: George Joseph <gjoseph@digium.com>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2007-06-08, 2010-08-30, 2013-03-27, 2016-04-20, 2017-10-26, 2018-04-19, 2019-04-02, 2019-09-22, 2019-10-08
-self-signatures SubkeyBinding: 2007-06-08, 2010-08-30, 2013-03-27, 2016-04-20, 2017-10-26, 2018-04-19, 2019-04-02, 2019-10-08
+           UserID: George Joseph <gjoseph@sangoma.com>
+self-signatures GenericCertification: 2010-08-30, 2013-03-27, 2013-03-28, 2016-04-20, 2016-04-25, 2016-05-13, 2017-04-05, 2017-10-26, 2018-04-19, 2019-10-08
+self-signatures PositiveCertification: 2007-06-08, 2010-08-30, 2013-03-27, 2016-04-20, 2017-04-05, 2017-10-26, 2018-04-19, 2019-04-02, 2019-09-22, 2019-10-08, 2021-06-15
+self-signatures SubkeyBinding: 2007-06-08, 2010-08-30, 2013-03-27, 2016-04-20, 2017-04-05, 2017-10-26, 2018-04-19, 2019-04-02, 2019-10-08
+third-party GenericCertification: 24
```

## Verification with the refreshed keyring

```
$ sqv ... asterisk-23.5.0.tar.gz
F2FC93DB7587BD1FB49E045A5D984BE337191CE7
rc=0
```

