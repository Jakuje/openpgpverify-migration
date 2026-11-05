# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show mingw-nettle`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- `nettle-release-keyring.gpg` was in the lookaside cache, which a PR cannot update, so it moves into git (its line in `sources` is dropped)
- replaced keyring `nettle-release-keyring.gpg` with `nettle-release-keyring.asc` from https://keys.openpgp.org/vks/v1/by-fingerprint/343C2FF0FBEE5EC2EDBEF399F3599FF828C67298#/nettle-release-keyring.asc; its `Source` line is now that URL (see below)
- Release bumped (`3%{?dist}` → `4%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-23 at dist-git commit `99f0fd0fa8fc` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. The key owner has updated the key since: the copy at https://keys.openpgp.org/vks/v1/by-fingerprint/343C2FF0FBEE5EC2EDBEF399F3599FF828C67298#/nettle-release-keyring.asc has the same fingerprint(s) and verifies the release with sqv. This PR replaces the file with that copy, byte for byte, named like the URL, which becomes its `Source`:

```
curl -fsSL -o nettle-release-keyring.asc 'https://keys.openpgp.org/vks/v1/by-fingerprint/343C2FF0FBEE5EC2EDBEF399F3599FF828C67298'
```

Fingerprints (unchanged):

- `343C2FF0FBEE5EC2EDBEF399F3599FF828C67298`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/nettle-release-keyring.gpg
+++ upstream/nettle-release-keyring.gpg
@@ -1,16 +1,10 @@
       Fingerprint: 343C2FF0FBEE5EC2EDBEF399F3599FF828C67298
-                   Invalid: The primary key is not live: Expired on 2025-01-15T17:12:43Z
-  Expiration time: 2025-01-15 17:12:43 UTC (creation time + 12years 7days 21h 46m 16s)
+  Expiration time: 2030-06-25 18:39:13 UTC (creation time + 17years 5months 16days 12h 24m 46s)
         Key flags: certification, signing
            Subkey: 48C9DE74746361F8617018347520153007F35B23
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-01-15T17:12:43Z
-  Expiration time: 2025-01-15 17:21:19 UTC (creation time + 12years 7days 21h 54m 52s)
+  Expiration time: 2030-06-25 18:40:52 UTC (creation time + 17years 5months 16days 12h 26m 25s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Niels Möller <nisse@lysator.liu.se>
-self-signatures PositiveCertification: 2013-01-07, 2020-01-17
-self-signatures SubkeyBinding: 2013-01-07, 2020-01-17
-third-party CasualCertification: 7
+self-signatures PositiveCertification: 2013-01-07, 2020-01-17, 2025-06-26
+self-signatures SubkeyBinding: 2013-01-07, 2020-01-17, 2025-06-26
 third-party CertificationRevocation: 1
-third-party GenericCertification: 16
-third-party PersonaCertification: 1
-third-party PositiveCertification: 3
```

This copy is from keys.openpgp.org, looked up by fingerprint, so it is the same key the old file held. If the project publishes the key somewhere you prefer, that URL works as well, as long as the copy verifies this release.

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
