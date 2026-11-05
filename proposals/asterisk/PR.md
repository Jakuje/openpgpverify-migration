# Verify source signatures with openpgpverify

This switches the upstream source signature check from a direct GnuPG call (`gpgv2`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The spec called GnuPG itself instead of using `%gpgverify`; the check becomes one `%openpgpverify` call with the same keyring, signature and data.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- the direct `gpgv2` call is replaced by `%{openpgpverify}` with the same keyring, signature and data
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- refreshed keyring `asterisk-gpgkeys.gpg` (see below)
- Release bumped (`%{?_rc||?_beta:0.}1%{?_rc:.rc%{_rc}}%{?_beta:.beta%{_beta}}%{?dist}` → `%{?_rc||?_beta:0.}1%{?_rc:.rc%{_rc}}%{?_beta:.beta%{_beta}}%{?dist}.1`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64, fedora-eln-x86_64, where even the current spec cannot install its build dependencies). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`gpgv2`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | pass |

Tested on 2026-11-05 at dist-git commit `40030608bf82` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` cannot read the keyring in dist-git: it is a GnuPG keybox, which `gpgv2` reads but sqv does not, so it is replaced with a plain OpenPGP keyring. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR replaces the keyring with the keyserver copy. No key was added or removed. Please check the fingerprint against upstream:

- `F2FC93DB7587BD1FB49E045A5D984BE337191CE7`
- `0F77FB5D216A02390B4C51DB7C2C8A8BCB3F61BD`
- `57E769BC37906C091E7F641F6CB44E557BD982D8`
- `551F29104B2106080C6C2851073B0C1FC9B2E352`
- `639D932D5170532F8C200CCD9C59F000777DCC45`
- `CDBEE4CC699E200EB4D46BB79E76E3A42341CE04`
- `80CEBC345EC9FF529B4B7B808438CBA18D0CAA72`
- `21A91EB1F012252993E9BF4A368AB332B59975F3`

The refresh, as run (the spec comment above the `Source` line has the same command, for the next refresh):

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

What changed in the certificate (`sq inspect`):

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

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10. It is not in EPEL 8, so if this spec is still used there, keep `%gpgverify` on that branch.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
