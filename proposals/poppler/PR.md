# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show poppler`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- updated `armored-keys.asc` to the current upstream copy from the URL in the spec (see below)

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64, fedora-eln-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-12 at dist-git commit `ab357b7d0ee5` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. Upstream has updated the key since: the copy at the URL the spec names for it has the same fingerprint(s) and verifies the release with sqv. This PR replaces the file with that copy, byte for byte:

```
curl -fsSL -o armored-keys.asc https://pgp.surfnet.nl/pks/lookup?op=get&search=0xCA262C6C83DE4D2FB28A332A3A6A4DB839EAA6D7
```

Fingerprints (unchanged):

- `CA262C6C83DE4D2FB28A332A3A6A4DB839EAA6D7`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/armored-keys.asc
+++ upstream/armored-keys.asc
@@ -1,13 +1,12 @@
       Fingerprint: CA262C6C83DE4D2FB28A332A3A6A4DB839EAA6D7
-                   Invalid: The primary key is not live: Expired on 2023-08-19T21:59:58Z
-  Expiration time: 2023-08-19 21:59:58 UTC (creation time + 6years 11months 13days 1h 24m 48s)
+  Expiration time: 2027-09-07 21:20:59 UTC (creation time + 11years 1day 14h 55m 25s)
         Key flags: certification, signing
            Subkey: 8692A42FB1A8B666C51053919D17D97FD8224750
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2023-08-19T21:59:58Z
-  Expiration time: 2021-08-13 21:31:53 UTC (creation time + 4years 11months 7days 12h 56m 43s)
+  Expiration time: 2027-09-07 10:00:03 UTC (creation time + 11years 1day 3h 34m 29s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Albert Astals Cid <aacid@kde.org>
-self-signatures PositiveCertification: 2016-09-05, 2018-05-16, 2018-07-31, 2019-08-14, 2020-07-28, 2021-08-01, 2022-08-18
-self-signatures SubkeyBinding: 2016-09-05, 2018-07-31, 2019-08-14, 2020-07-28
+self-signatures PositiveCertification: 2016-09-05, 2018-05-16, 2018-07-31, 2019-08-14, 2020-07-28, 2021-08-01, 2022-08-18, 2026-04-20
+self-signatures SubkeyBinding: 2016-09-05, 2018-07-31, 2019-08-14, 2020-07-28, 2026-04-20
+third-party CasualCertification: 1
 third-party GenericCertification: 13
 third-party PositiveCertification: 1
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: the spec has a `%check` section or uses gpg elsewhere, and tests may need it. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
