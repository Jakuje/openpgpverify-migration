# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show libtalloc`).

This switches the upstream source signature check from a direct GnuPG call (`gpgv2`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The spec called GnuPG itself instead of using `%gpgverify`; the check becomes one `%openpgpverify` call with the same keyring, signature and data.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- the direct `gpgv2` call is replaced by `%{openpgpverify}` with the same keyring, signature and data
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- updated `talloc.keyring` to the current upstream copy from the URL in the spec (see below)

### Testing

The current and the changed spec were both run through `rpmbuild -bc` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`gpgv2`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-26 at dist-git commit `41b7fe1706b3` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (SHA-1 key self-signatures), while `gpgv2` ignores that. Upstream has updated the key since: the copy at https://download.samba.org/pub/samba/samba-pubkey.asc#/talloc.keyring has the same fingerprint(s) and also holds other keys upstream publishes there and verifies the release with sqv. This PR replaces the file with that copy, byte for byte:

```
curl -fsSL -o talloc.keyring 'https://download.samba.org/pub/samba/samba-pubkey.asc'
```

Fingerprints (unchanged):

- `9147A339719518EE9011BCB54793916113084025`

Added to the keyring, because upstream's file holds them too; this also means a release signed with one of them will verify:

- `81F5E2832BD2545A1897B713AA99442FB680B620`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/talloc.keyring
+++ upstream/talloc.keyring
@@ -1,6 +1,18 @@
+      Fingerprint: 81F5E2832BD2545A1897B713AA99442FB680B620
+  Expiration time: 2027-12-12 17:06:40 UTC (creation time + 6years 11months 20days 20h 46m 4s)
+        Key flags: certification, signing
+           Subkey: 8ECB3E1AD3C66464249027DE97EF9386FBFD4002
+  Expiration time: 2027-12-12 17:09:32 UTC (creation time + 6years 11months 20days 20h 48m 56s)
+        Key flags: transport encryption, data-at-rest encryption
+           UserID: Samba Distribution Verification Key <samba-bugs@samba.org>
       Fingerprint: 9147A339719518EE9011BCB54793916113084025
-                   Invalid: No binding signature at time 2026-11-05T09:38:25Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2027-12-13 12:18:24 UTC (creation time + 16years 10months 30days 6h 51m 33s)
+        Key flags: certification, signing
+           Subkey: 541FB94987D491A3C201D8B1B1DD08BF65F64DAB
+  Expiration time: 2027-12-13 12:18:38 UTC (creation time + 16years 10months 30days 6h 51m 47s)
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Samba Library Distribution Key <samba-bugs@samba.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2015-04-29
+self-signatures PositiveCertification: 2011-01-12, 2012-01-21, 2013-01-27, 2014-03-20, 2015-04-29, 2016-05-06, 2017-06-02, 2018-06-26, 2019-07-03, 2020-07-09, 2020-12-21, 2022-12-19, 2023-12-18, 2024-10-15, 2025-12-12, 2025-12-13
+self-signatures SubkeyBinding: 2025-12-12, 2025-12-13
+third-party GenericCertification: 3
+third-party PositiveCertification: 1
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the changed spec does not get past the signature check. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.
- The verification runs outside `%prep`. Moving it to the start of `%prep` would check the sources before anything else uses them.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
