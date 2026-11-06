# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show libextractor`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- replaced the keyring with the signing key from keyservers, keyring `libextractor-keyring.pgp`, which the `Source` line now names (see below); the comment above its `Source` line shows the commands
- `gnu-keyring.gpg` is no longer used; its line in `sources` is dropped

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-26 at dist-git commit `b5ca0d7e72ea` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` cannot use the keyring in dist-git: it holds 10 v3 (PGP 2) keys, which Sequoia does not parse, so sqv rejects the whole file (GnuPG skips such keys silently). This PR replaces it with the keyserver copy of the key that signed the release, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), with exactly this command (also in the comment above the keyring's `Source` line, for the next update):

```
sq --home=none network keyserver search D8423BCB326C7907033929C7939E6BE1E29FC3CC --output libextractor-keyring.pgp --overwrite
```

Please check the fingerprint against upstream:

- `D8423BCB326C7907033929C7939E6BE1E29FC3CC`

Dropped from the keyring (not used for the current release; add them back if releases may be signed with them):

- the other 541 certificates of `gnu-keyring.gpg`

What changed in the signing certificate (`sq inspect`):

```diff
--- dist-git/gnu-keyring.gpg (as GnuPG reads it)
+++ new/libextractor-keyring.pgp
@@ -1,4833 +1,3 @@
-      Fingerprint: 4B0261875C03D6B12E31766609DF2DC9BE216115
-                   Invalid: No binding signature at time 2026-11-06T09:25:40Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: 6EEBDFC5CDEB726F09A8C51A08991F437126024F
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-06T09:25:40Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Francesco Potorti` <F.Potorti@cnuce.cnr.it>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Francesco Potorti` <pot@gnu.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Francesco Potorti` <pot@potorti.it>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Francesco Potorti` <pot@softwarelibero.it>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Francesco Potortì <F.Potorti@cnuce.cnr.it>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Francesco Potortì <pot@gnu.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Francesco Potortì <pot@potorti.it>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Francesco Potortì <pot@softwarelibero.it>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-      Fingerprint: 6F818B215E159EF3FA26B0BE624DC565135EA668
-                   Invalid: No binding signature at time 2026-11-06T09:25:40Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: 04C26DD3834A1AB3A3CAB2D4879A7C37B1B10ED6
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-06T09:25:40Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Richard Stallman (Chief GNUisance) <rms@gnu.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-      Fingerprint: D70D9D25AF3837A5909A4683FDD2DEACD333CBA1
-                   Invalid: No binding signature at time 2026-11-06T09:25:40Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: 3CF13F0585B52367EFAA47C8F8B0A218A3DC3293
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-06T09:25:40Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: 775E8866695B180CD94CB471D77FFDE1B9AB9A16
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-06T09:25:40Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Jim Meyering <jim@meyering.net>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Jim Meyering <meyering@ascend.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Jim Meyering <meyering@gnu.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Jim Meyering <meyering@lucent.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Jim Meyering <meyering@na-net.ornl.gov>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Jim Meyering <meyering@pobox.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Jim Meyering <meyering@redhat.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-      Fingerprint: AD63DAA9CE7A044434DF3917B93F60C6B5C4CE13
-                   Invalid: No binding signature at time 2026-11-06T09:25:40Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: 52B6169AD13DBAA070A5021A19A086AB749EDE35
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-06T09:25:40Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Paul Eggert <eggert@cs.ucla.edu>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-      Fingerprint: FCA086150211941A2AB9FA663859C03B2E236E47
-                   Invalid: No binding signature at time 2026-11-06T09:25:40Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: A4C50B3041EF94FE2E19FD17C7B3DCCE8E0DA454
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-06T09:25:40Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Alexandre Duret-Lutz <Alexandre.Duret-Lutz@lip6.fr>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Alexandre Duret-Lutz <Alexandre.Duret-Lutz@src.lip6.fr>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Alexandre Duret-Lutz <adl@gnu.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Alexandre Duret-Lutz <adl@src.lip6.fr>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Alexandre Duret-Lutz <adl@users.sourceforge.net>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Alexandre Duret-Lutz <adl@va-et-vient.net>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Alexandre Duret-Lutz <aduret@src.lip6.fr>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Alexandre Duret-Lutz <duret_g@epita.fr>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Alexandre Duret-Lutz <duret_g@lrde.epita.fr>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-      Fingerprint: 2FFA9AFC5994B8A18CC9741A2F7771E469B44003
-                   Invalid: No binding signature at time 2026-11-06T09:25:40Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: F1E0B1476CA38FDA3169ACA6513A435A6776F180
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-06T09:25:40Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Claudio Fontana (temp) <sick_soul@users.sourceforge.net>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-      Fingerprint: FE4E00D957D6B28B86F75CA17E2D65C109718317
-                   Invalid: No binding signature at time 2026-11-06T09:25:40Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: 84307B0309AFC95E6EB5441A4CB15AC095524C0B
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-06T09:25:40Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Bruno Haible (Open Source Development) <bruno@clisp.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-      Fingerprint: 11FB137388802517E3C902AB55148237194D9EED
-                   Invalid: No binding signature at time 2026-11-06T09:25:40Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: 3A1FE3FF769D29C6BCFC0AFAEDB032C664AF595F
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-06T09:25:40Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Alvaro Lopez Ortega (alo) <alvaro@godsmaze.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-      Fingerprint: 8EF041155AFB37AFACC726F310709966E099F769
-                   Invalid: No binding signature at time 2026-11-06T09:25:40Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: 9FFDB84630F82DDE4BE5FAB67DFF7D8CCBA96F7D
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-06T09:25:40Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Tokio Kikuchi <tkikuchi@is.kochi-u.ac.jp>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-      Fingerprint: 935E7C692EAA7E742CCD35D2F6D36D31E5D02E42
-                   Invalid: No binding signature at time 2026-11-06T09:25:40Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: 51ABB30CC01A9F92D115BF7A691EDFBF24751B64
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-06T09:25:40Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Christian Grothoff <grothoff@cs.purdue.edu>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-      Fingerprint: A2B56CCB42220C06481335BAD17BF2305981E818
-                   Invalid: No binding signature at time 2026-11-06T09:25:40Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: 635A6CB34BE481B93FE8C859BE29AE845676121E
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-06T09:25:40Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Andrew Makhorin <mao@mai2.rcnet.ru>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-      Fingerprint: 325F650C4C2B6AD58807327A3602B07F55D0C732
-                   Invalid: No binding signature at time 2026-11-06T09:25:40Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: 6E3ED4689F1B56FA16AC6A6C7EF0463856DFFBBA
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-06T09:25:40Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Sergey Poznyakoff (Gray) <gray@mirddin.farlep.net>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Sergey Poznyakoff <gray@gnu.org.ua>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-           UserID: Sergey Poznyakoff <gray@gnu.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-      Fingerprint: A78EDBD82850EDFE8C7F9850A309D67919A22547
-                   Invalid: No binding signature at time 2026-11-06T09:25:40Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           Subkey: 4A0534FA40A901BA8E81C4100EA6865F6EB957B7
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-06T09:25:40Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Wojciech Polak <polak@gnu.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-      Fingerprint: 1E90AEA8D51158F094E5B106722024E97B2FD4B0
-                   Invalid: No binding signature at time 2026-11-06T09:25:40Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
-           UserID: Mauro Tortonesi (GNU Wget Maintain
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the changed spec does not get past the signature check. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
