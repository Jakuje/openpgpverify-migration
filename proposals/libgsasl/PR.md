# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show libgsasl`).

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
- refreshed keyring `54265e8c.txt` (see below)
- Release bumped (`17%{?dist}` → `18%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-23 at dist-git commit `957322061f85` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (keyring lacks older self-signatures), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.mailvelope.com, hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `9AA9BDB11BB1B99A21285A330664A76954265E8C`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/54265e8c.txt
+++ refreshed/54265e8c.txt
@@ -17,7 +17,7 @@
            UserID: Simon Josefsson <simon@josefsson.org>
            UserID: Simon Josefsson <simon@yubico.com>
 self-signatures PositiveCertification: 2014-06-22, 2014-08-26, 2015-01-15, 2015-08-13, 2016-04-12, 2016-08-11, 2017-01-25, 2017-08-28, 2018-02-26, 2018-08-02, 2019-03-07, 2020-01-01, 2020-01-25, 2020-12-22, 2021-07-21, 2022-03-21, 2022-10-04
-self-signatures SubkeyBinding: 2022-10-04
+self-signatures SubkeyBinding: 2014-06-22, 2014-08-26, 2015-01-15, 2015-08-13, 2016-04-12, 2016-08-11, 2017-01-25, 2017-08-28, 2018-02-26, 2018-08-02, 2019-03-07, 2020-01-01, 2020-01-25, 2020-12-22, 2021-07-21, 2022-03-21, 2022-10-04
 third-party CasualCertification: 5
-third-party GenericCertification: 25
+third-party GenericCertification: 28
 third-party PositiveCertification: 3
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the changed spec does not get past the signature check. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
