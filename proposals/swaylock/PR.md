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
- replaced keyring `gpgkey-E88F5E48.asc` with `gpgkey-0FDE7BE0E88F5E48.asc` from https://keys.openpgp.org/vks/v1/by-fingerprint/34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48#/gpgkey-0FDE7BE0E88F5E48.asc; its `Source` line is now that URL (see below)

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | pass |

Tested on 2026-11-04 at dist-git commit `1e9af1a2f3ab` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (verification fails), while `%gpgverify` ignores that. Upstream has updated the key since: the copy at https://keys.openpgp.org/vks/v1/by-fingerprint/34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48#/gpgkey-0FDE7BE0E88F5E48.asc has the same fingerprint(s) and verifies the release with sqv. This PR replaces the file with that copy, byte for byte, named like the URL, which becomes its `Source`:

```
curl -fsSL -o gpgkey-0FDE7BE0E88F5E48.asc 'https://keys.openpgp.org/vks/v1/by-fingerprint/34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48'
```

Fingerprints (unchanged):

- `34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/gpgkey-E88F5E48.asc
+++ upstream/gpgkey-E88F5E48.asc
@@ -1,11 +1,10 @@
       Fingerprint: 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48
-                   Invalid: The primary key is not live: Expired on 2022-03-10T17:55:59Z
-  Expiration time: 2022-03-10 17:55:59 UTC (creation time + 5years 11months 7days 17h 54m 5s)
+  Expiration time: 2027-04-12 16:35:43 UTC (creation time + 11years 10days 43m 25s)
         Key flags: certification, signing
            Subkey: 3842522FEB127E044BC92BEA10D018335A0B5D8E
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-03-10T17:55:59Z
-  Expiration time: 2022-03-10 17:56:33 UTC (creation time + 5years 11months 7days 17h 54m 39s)
+  Expiration time: 2027-04-12 16:35:24 UTC (creation time + 11years 10days 43m 6s)
         Key flags: transport encryption, data-at-rest encryption
+           UserID: Simon Ser <contact@emersion.fr>
            UserID: emersion <contact@emersion.fr>
-self-signatures PositiveCertification: 2021-03-10
-self-signatures SubkeyBinding: 2021-03-10
+self-signatures PositiveCertification: 2016-04-01, 2017-04-01, 2018-04-02, 2019-03-11, 2019-04-08, 2020-03-04, 2021-03-10, 2022-03-30, 2023-04-01, 2023-04-21, 2024-04-03, 2025-04-12, 2026-04-12
+self-signatures SubkeyBinding: 2016-04-01, 2017-04-01, 2018-04-02, 2019-04-08, 2020-03-04, 2021-03-10, 2022-03-30, 2023-04-01, 2024-04-03, 2025-04-12, 2026-04-12
```

Why keys.openpgp.org and not the WKD copy at emersion.fr: the key is extended every April, and the WKD copy carries only the newest self-signatures (now from 2026-04-12). sqv needs a binding that was valid when the release was signed, so the WKD copy fails for any release signed before the latest extension. keys.openpgp.org keeps the whole self-signature history back to 2016, so the file verifies older and newer releases alike, and it can be fetched again with the same URL after the next extension.

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is dropped too. To check that nothing else needs it, the changed spec was built completely (`rpmbuild -bb`; the spec has no `%check`) in a chroot with gnupg2 and gpgverify removed, and the build log doesn't mention gpg.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
