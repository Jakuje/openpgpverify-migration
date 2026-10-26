# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show skribilo`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- refreshed keyring `arunisaac.pub` (see below)
- Release bumped (`3%{?dist}` → `4%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-23 at dist-git commit `1eb78a8eb562` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `7F730343F2F09F3C77BF79D32E25EE8B61802BB3`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/arunisaac.pub
+++ refreshed/arunisaac.pub
@@ -1,10 +1,8 @@
       Fingerprint: 7F730343F2F09F3C77BF79D32E25EE8B61802BB3
-                   Invalid: The primary key is not live: Expired on 2024-03-01T09:44:40Z
-  Expiration time: 2024-03-01 09:44:40 UTC (creation time + 10years 5months 23days 1m 52s)
+  Expiration time: 2027-03-01 22:11:41 UTC (creation time + 13years 5months 22days 18h 28m 53s)
         Key flags: certification, signing
            Subkey: B7ACCF781EB7E021FD8CB1CAA6E8C999B91F5347
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2024-03-01T09:44:40Z
-  Expiration time: 2024-03-01 09:45:10 UTC (creation time + 10years 5months 23days 2m 22s)
+  Expiration time: 2027-03-01 22:13:10 UTC (creation time + 13years 5months 22days 18h 30m 22s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Arun I (My personal key) <theroarofthedragon@gmail.com>
                    Revoked:
@@ -12,6 +10,6 @@
                    because: SHA1 is not considered secure
            UserID: Arun I <arunisaac@systemreboot.net>
 self-signatures CertificationRevocation: 2016-09-23
-self-signatures PositiveCertification: 2013-09-07, 2015-10-25, 2017-03-20, 2018-03-21, 2020-03-19, 2023-03-02
-self-signatures SubkeyBinding: 2023-03-02
+self-signatures PositiveCertification: 2013-09-07, 2015-10-25, 2017-03-20, 2018-03-21, 2019-03-19, 2020-03-19, 2021-03-19, 2022-03-12, 2023-03-02, 2024-03-01, 2025-03-01, 2026-03-01
+self-signatures SubkeyBinding: 2013-09-07, 2015-03-20, 2016-03-20, 2017-03-20, 2018-03-21, 2019-03-19, 2020-03-19, 2021-03-19, 2022-03-12, 2023-03-02, 2024-03-01, 2025-03-01, 2026-03-01
 third-party GenericCertification: 1
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the changed spec does not get past the signature check. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
