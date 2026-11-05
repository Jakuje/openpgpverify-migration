# Verify source signatures with openpgpverify

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
- updated `arunisaac.pub` to the current upstream copy from the URL in the spec (see below)
- Release bumped (`3%{?dist}` → `4%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | pass |

Tested on 2026-11-05 at dist-git commit `1eb78a8eb562` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (verification fails), while `%gpgverify` ignores that. The key owner has updated the key since: the copy at https://keys.openpgp.org/vks/v1/by-fingerprint/7F730343F2F09F3C77BF79D32E25EE8B61802BB3#/arunisaac.pub has the same fingerprint(s) and verifies the release with sqv. This PR replaces the file with that copy, byte for byte:

```
curl -fsSL -o arunisaac.pub 'https://keys.openpgp.org/vks/v1/by-fingerprint/7F730343F2F09F3C77BF79D32E25EE8B61802BB3'
```

Fingerprints (unchanged):

- `7F730343F2F09F3C77BF79D32E25EE8B61802BB3`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/arunisaac.pub
+++ upstream/arunisaac.pub
@@ -1,17 +1,11 @@
       Fingerprint: 7F730343F2F09F3C77BF79D32E25EE8B61802BB3
-                   Invalid: The primary key is not live: Expired on 2024-03-01T09:44:40Z
-  Expiration time: 2024-03-01 09:44:40 UTC (creation time + 10years 5months 23days 1m 52s)
+                   Invalid: The primary key is not live: Expired on 2026-03-01T19:09:07Z
+  Expiration time: 2026-03-01 19:09:07 UTC (creation time + 12years 5months 22days 21h 26m 19s)
         Key flags: certification, signing
            Subkey: B7ACCF781EB7E021FD8CB1CAA6E8C999B91F5347
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2024-03-01T09:44:40Z
-  Expiration time: 2024-03-01 09:45:10 UTC (creation time + 10years 5months 23days 2m 22s)
+                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-03-01T19:09:07Z
+  Expiration time: 2026-03-01 19:09:57 UTC (creation time + 12years 5months 22days 21h 27m 9s)
         Key flags: transport encryption, data-at-rest encryption
-           UserID: Arun I (My personal key) <theroarofthedragon@gmail.com>
-                   Revoked:
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Arun I <arunisaac@systemreboot.net>
-self-signatures CertificationRevocation: 2016-09-23
-self-signatures PositiveCertification: 2013-09-07, 2015-10-25, 2017-03-20, 2018-03-21, 2020-03-19, 2023-03-02
-self-signatures SubkeyBinding: 2023-03-02
-third-party GenericCertification: 1
+self-signatures PositiveCertification: 2015-10-25, 2017-03-20, 2018-03-21, 2020-03-19, 2025-03-01
+self-signatures SubkeyBinding: 2025-03-01
```

This copy is from keys.openpgp.org, looked up by fingerprint, so it is the same key the old file held. If the project publishes the key somewhere you prefer, that URL works as well, as long as the copy verifies this release.

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is dropped too. To check that nothing else needs it, the changed spec was built completely (`rpmbuild -bb`, including `%check`) in a chroot with gnupg2 and gpgverify removed, and neither the build log nor the test files in the sources mention gpg.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
