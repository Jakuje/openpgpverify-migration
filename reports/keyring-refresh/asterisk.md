# Keyring refresh for asterisk

**Status: proposed**

Failing call: `--keyring=/builddir/new/asterisk-gpgkeys.gpg --signature=/builddir/new/asterisk-23.5.0.tar.gz.asc --data=/builddir/new/asterisk-23.5.0.tar.gz`

Phase 1 reason: `keybox`

## asterisk-gpgkeys.gpg

- **format: GnuPG keybox, converted to an OpenPGP keyring (sqv does not read keyboxes)**
- certificates: F2FC93DB7587BD1FB49E045A5D984BE337191CE7, 0F77FB5D216A02390B4C51DB7C2C8A8BCB3F61BD, 57E769BC37906C091E7F641F6CB44E557BD982D8, 551F29104B2106080C6C2851073B0C1FC9B2E352, 639D932D5170532F8C200CCD9C59F000777DCC45, CDBEE4CC699E200EB4D46BB79E76E3A42341CE04, 80CEBC345EC9FF529B4B7B808438CBA18D0CAA72, 21A91EB1F012252993E9BF4A368AB332B59975F3
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 23332 → 46306 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network keyserver search \
  F2FC93DB7587BD1FB49E045A5D984BE337191CE7 \
  0F77FB5D216A02390B4C51DB7C2C8A8BCB3F61BD \
  57E769BC37906C091E7F641F6CB44E557BD982D8 \
  551F29104B2106080C6C2851073B0C1FC9B2E352 \
  639D932D5170532F8C200CCD9C59F000777DCC45 \
  CDBEE4CC699E200EB4D46BB79E76E3A42341CE04 \
  80CEBC345EC9FF529B4B7B808438CBA18D0CAA72 \
  21A91EB1F012252993E9BF4A368AB332B59975F3 \
  --output asterisk-gpgkeys.gpg --overwrite
```

```diff
--- dist-git/asterisk-gpgkeys.gpg (exported from keybox)
+++ refreshed/asterisk-gpgkeys.gpg
@@ -1,8 +1,3 @@
-      Fingerprint: F2FC93DB7587BD1FB49E045A5D984BE337191CE7
-        Key flags: certification, signing
-           Subkey: FBD813C655FE8E138E2D6C57D2A823286A220BEE
-        Key flags: transport encryption, data-at-rest encryption
-           UserID: Asterisk Development Team <asteriskteam@digium.com>
       Fingerprint: 0F77FB5D216A02390B4C51DB7C2C8A8BCB3F61BD
                    Invalid: No binding signature at time 2026-11-05T18:17:43Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
            Subkey: 375C5BCC3D96E743F8F6AC85A16617C1EF507C8C
@@ -12,15 +7,16 @@
            UserID: Chris Savinovich <csavinovich@digium.com>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-      Fingerprint: 57E769BC37906C091E7F641F6CB44E557BD982D8
-                   Invalid: No binding signature at time 2026-11-05T18:17:43Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: 7E4860121BD5B645CEE218A6F0556C24253C5733
+      Fingerprint: 21A91EB1F012252993E9BF4A368AB332B59975F3
+        Key flags: certification, signing
+           Subkey: 993583DE8CB2CEB44ACDE5EBEE5B5FF60C3CF379
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-05T18:17:43Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Richard Mudgett <rmudgett@digium.com>
+                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
+           UserID: George Joseph <gjoseph@digium.com>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
+           UserID: George Joseph <gjoseph@sangoma.com>
       Fingerprint: 551F29104B2106080C6C2851073B0C1FC9B2E352
                    Invalid: No binding signature at time 2026-11-05T18:17:43Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
            Subkey: 0571D2EB82005A576B6006AE16CFCE9A1884FB3A
@@ -30,25 +26,22 @@
            UserID: Ben Ford <bford@digium.com>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-      Fingerprint: 639D932D5170532F8C200CCD9C59F000777DCC45
+      Fingerprint: 57E769BC37906C091E7F641F6CB44E557BD982D8
                    Invalid: No binding signature at time 2026-11-05T18:17:43Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: 4445F78B5F17259C63C31A71F3AAF493D520EE46
+           Subkey: 7E4860121BD5B645CEE218A6F0556C24253C5733
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
                    Invalid: primary key: No binding signature at time 2026-11-05T18:17:43Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Kevin Harwell <kharwell@digium.com>
+           UserID: Richard Mudgett <rmudgett@digium.com>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-      Fingerprint: CDBEE4CC699E200EB4D46BB79E76E3A42341CE04
+      Fingerprint: 639D932D5170532F8C200CCD9C59F000777DCC45
                    Invalid: No binding signature at time 2026-11-05T18:17:43Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: CC2B11EA5C5D7ACA0CFA924F4693ED1973774BE5
+           Subkey: 4445F78B5F17259C63C31A71F3AAF493D520EE46
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
                    Invalid: primary key: No binding signature at time 2026-11-05T18:17:43Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Joshua Colp <jcolp@digium.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Joshua Colp <jcolp@joshua-colp.com>
+           UserID: Kevin Harwell <kharwell@digium.com>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
       Fingerprint: 80CEBC345EC9FF529B4B7B808438CBA18D0CAA72
@@ -60,14 +53,24 @@
            UserID: Matthew Fredrickson <creslin@digium.com>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-      Fingerprint: 21A91EB1F012252993E9BF4A368AB332B59975F3
+      Fingerprint: CDBEE4CC699E200EB4D46BB79E76E3A42341CE04
                    Invalid: No binding signature at time 2026-11-05T18:17:43Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: 993583DE8CB2CEB44ACDE5EBEE5B5FF60C3CF379
+           Subkey: CC2B11EA5C5D7ACA0CFA924F4693ED1973774BE5
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
                    Invalid: primary key: No binding signature at time 2026-11-05T18:17:43Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: George Joseph <gjoseph@digium.com>
+           UserID: Joshua Colp <jcolp@digium.com>
+                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
+                   because: SHA1 is not considered secure
+           UserID: Joshua Colp <jcolp@joshua-colp.com>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2007-06-08, 2010-08-30, 2013-03-27, 2016-04-20, 2017-10-26, 2018-04-19, 2019-04-02, 2019-09-22, 2019-10-08
-self-signatures SubkeyBinding: 2007-06-08, 2010-08-30, 2013-03-27, 2016-04-20, 2017-10-26, 2018-04-19, 2019-04-02, 2019-10-08
+      Fingerprint: F2FC93DB7587BD1FB49E045A5D984BE337191CE7
+        Key flags: certification, signing
+           Subkey: FBD813C655FE8E138E2D6C57D2A823286A220BEE
+        Key flags: transport encryption, data-at-rest encryption
+           UserID: Asterisk Development Team <asteriskteam@digium.com>
+self-signatures GenericCertification: 2010-08-30, 2013-03-27, 2013-03-28, 2016-04-20, 2016-04-25, 2016-05-13, 2017-04-05, 2017-10-26, 2018-04-19, 2019-10-08
+self-signatures PositiveCertification: 2007-06-08, 2010-08-30, 2013-03-27, 2016-04-20, 2017-04-05, 2017-10-26, 2018-04-19, 2019-04-02, 2019-10-08, 2021-06-15
+self-signatures SubkeyBinding: 2007-06-08, 2010-08-30, 2013-03-27, 2016-04-20, 2017-04-05, 2017-10-26, 2018-04-19, 2019-04-02, 2019-10-08
+third-party GenericCertification: 24
```

## Verification with the refreshed keyring

```
$ sqv ... asterisk-23.5.0.tar.gz
F2FC93DB7587BD1FB49E045A5D984BE337191CE7
rc=0
```

