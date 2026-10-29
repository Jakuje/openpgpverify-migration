# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show mingw-libidn2`).

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
- updated `B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE` to the current upstream copy from the URL in the spec (see below)
- Release bumped (`4%{?dist}` → `5%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-23 at dist-git commit `f08d63ff6ad2` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. Upstream has updated the key since: the copy at the URL the spec names for it has the same fingerprint(s) and verifies the release with sqv. This PR replaces the file with that copy, byte for byte:

```
curl -fsSL -o B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE https://keys.openpgp.org/vks/v1/by-fingerprint/B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
```

Fingerprints (unchanged):

- `B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
+++ upstream/B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
@@ -1,19 +1,15 @@
       Fingerprint: B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE
-                   Invalid: The primary key is not live: Expired on 2022-10-23T15:48:28Z
-  Expiration time: 2022-10-23 15:48:28 UTC (creation time + 3years 7months 3days 20h 15m 52s)
+  Expiration time: 2027-05-24 20:19:03 UTC (creation time + 8years 2months 3days 23h 34m 27s)
         Key flags: certification, signing
            Subkey: A3CC9C870B9D310ABAD4CF2F51722B08FE4745A2
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-10-23T15:48:28Z
-  Expiration time: 2022-10-23 15:48:47 UTC (creation time + 3years 7months 3days 20h 12m 46s)
+  Expiration time: 2027-05-24 20:14:47 UTC (creation time + 8years 2months 3days 23h 26m 46s)
         Key flags: signing
            Subkey: A9EC8F4D7F1E50ED3DEF49A902923D7EE76EBD60
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-10-23T15:48:28Z
-  Expiration time: 2022-10-23 15:48:36 UTC (creation time + 3years 7months 3days 20h 12m 58s)
+  Expiration time: 2027-05-24 20:14:47 UTC (creation time + 8years 2months 3days 23h 27m 9s)
         Key flags: transport encryption, data-at-rest encryption
            Subkey: CA7E37164342DF3133DF349780260EE8A9B92B2B
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-10-23T15:48:28Z
-  Expiration time: 2022-10-23 15:48:43 UTC (creation time + 3years 7months 3days 20h 12m 54s)
+  Expiration time: 2027-05-24 20:14:47 UTC (creation time + 8years 2months 3days 23h 26m 58s)
         Key flags: authentication
            UserID: Simon Josefsson <simon@josefsson.org>
-self-signatures PositiveCertification: 2019-03-20, 2019-10-23, 2020-05-27, 2020-12-22, 2021-07-21, 2022-03-21
-self-signatures SubkeyBinding: 2019-03-20, 2019-10-23, 2020-05-27, 2020-12-22, 2021-07-21, 2022-03-21
+self-signatures PositiveCertification: 2019-03-20, 2019-10-23, 2020-05-27, 2020-12-22, 2021-07-21, 2022-03-21, 2022-10-04, 2023-09-01, 2024-03-22, 2025-03-12, 2026-04-17, 2026-10-20
+self-signatures SubkeyBinding: 2019-03-20, 2019-10-23, 2020-05-27, 2020-12-22, 2021-07-21, 2022-03-21, 2022-10-04, 2024-03-22, 2025-03-12, 2026-04-16, 2026-10-20
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the changed spec does not get past the signature check. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
