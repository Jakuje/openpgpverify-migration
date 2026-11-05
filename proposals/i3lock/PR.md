# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show i3lock`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- dropped `BuildRequires:  gnupg2`, only needed for `%gpgverify`
- replaced keyring `gpgkey-424E14D703E7C6D43D9D6F364E7160ED4AC8EE1D.gpg` with `gpgkey-424E14D703E7C6D43D9D6F364E7160ED4AC8EE1D.asc` from https://keys.openpgp.org/vks/v1/by-fingerprint/424E14D703E7C6D43D9D6F364E7160ED4AC8EE1D#/gpgkey-424E14D703E7C6D43D9D6F364E7160ED4AC8EE1D.asc; its `Source` line is now that URL (see below)

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-22 at dist-git commit `ce83fae440ed` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. The key owner has updated the key since: the copy at https://keys.openpgp.org/vks/v1/by-fingerprint/424E14D703E7C6D43D9D6F364E7160ED4AC8EE1D#/gpgkey-424E14D703E7C6D43D9D6F364E7160ED4AC8EE1D.asc has the same fingerprint(s) and verifies the release with sqv. This PR replaces the file with that copy, byte for byte, named like the URL, which becomes its `Source`:

```
curl -fsSL -o gpgkey-424E14D703E7C6D43D9D6F364E7160ED4AC8EE1D.asc 'https://keys.openpgp.org/vks/v1/by-fingerprint/424E14D703E7C6D43D9D6F364E7160ED4AC8EE1D'
```

Fingerprints (unchanged):

- `424E14D703E7C6D43D9D6F364E7160ED4AC8EE1D`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/gpgkey-424E14D703E7C6D43D9D6F364E7160ED4AC8EE1D.gpg
+++ upstream/gpgkey-424E14D703E7C6D43D9D6F364E7160ED4AC8EE1D.gpg
@@ -1,8 +1,7 @@
       Fingerprint: 424E14D703E7C6D43D9D6F364E7160ED4AC8EE1D
-                   Invalid: The primary key is not live: Expired on 2022-05-05T11:36:21Z
-  Expiration time: 2022-05-05 11:36:21 UTC (creation time + 12years 11months 14days 6h 11m 58s)
+  Expiration time: 2030-01-21 19:42:26 UTC (creation time + 20years 8months 1day 21h 58m 51s)
         Key flags: certification, signing, authentication, transport encryption, data-at-rest encryption
            UserID: Michael Stapelberg (RENT-A-GURU) <michael@rent-a-guru.de>
            UserID: Michael Stapelberg <michael@stapelberg.de>
            UserID: Michael Stapelberg <stapelberg@debian.org>
-self-signatures PositiveCertification: 2017-05-06
+self-signatures PositiveCertification: 2009-05-21, 2012-03-28, 2014-04-27, 2017-05-06, 2020-05-21, 2025-01-22
```

This copy is from keys.openpgp.org, looked up by fingerprint, so it is the same key the old file held. If the project publishes the key somewhere you prefer, that URL works as well, as long as the copy verifies this release.

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
