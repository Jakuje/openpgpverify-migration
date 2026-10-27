# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show cgit`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (2 calls; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- updated `gpgkey-AB9942E6D4A4CFC3412620A749FC7012A5DE03AE.asc` to the current upstream copy from the URL in the spec (see below)
- Release bumped (`5%{?dist}` → `6%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 2 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-26 at dist-git commit `72263f147e2a` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. Upstream has updated the key since: the copy at the URL the spec names for it has the same fingerprint(s) and verifies the release with sqv. This PR replaces the file with that copy, byte for byte:

```
curl -fsSL -o gpgkey-AB9942E6D4A4CFC3412620A749FC7012A5DE03AE.asc https://www.zx2c4.com/keys/AB9942E6D4A4CFC3412620A749FC7012A5DE03AE.asc
```

Fingerprints (unchanged):

- `AB9942E6D4A4CFC3412620A749FC7012A5DE03AE`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/gpgkey-AB9942E6D4A4CFC3412620A749FC7012A5DE03AE.asc
+++ upstream/gpgkey-AB9942E6D4A4CFC3412620A749FC7012A5DE03AE.asc
@@ -1,14 +1,9 @@
       Fingerprint: AB9942E6D4A4CFC3412620A749FC7012A5DE03AE
-                   Invalid: The primary key is not live: Expired on 2022-02-11T13:41:11Z
-  Expiration time: 2022-02-11 13:41:11 UTC (creation time + 11years 26days 20h 58m 15s)
+  Expiration time: 2027-03-31 19:17:27 UTC (creation time + 16years 2months 13days 23h 27m 19s)
         Key flags: certification, signing
            Subkey: 472A073D982F00805C932395D4F7A95DFB1EFB7F
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-02-11T13:41:11Z
-  Expiration time: 2022-02-11 13:41:39 UTC (creation time + 11years 26days 20h 58m 43s)
+  Expiration time: 2027-03-31 19:17:36 UTC (creation time + 16years 2months 13days 23h 27m 28s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Jason A. Donenfeld <Jason@zx2c4.com>
-self-signatures PositiveCertification: 2011-01-15, 2013-03-29, 2013-10-31, 2014-11-07, 2015-03-18, 2017-02-10, 2021-02-11
-self-signatures SubkeyBinding: 2021-02-11
-third-party CasualCertification: 1
-third-party GenericCertification: 19
-third-party PositiveCertification: 7
+self-signatures PositiveCertification: 2024-03-31
+self-signatures SubkeyBinding: 2024-03-31
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the changed spec does not get past the signature check. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
