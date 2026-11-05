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
- dropped `BuildRequires: gnupg2`, only needed for `%gpgverify`
- `newsboat.pgp` was in the lookaside cache, which a PR cannot update, so it moves into git (its line in `sources` is dropped)
- replaced keyring `newsboat.pgp` with `newsboat.asc` from https://keys.openpgp.org/vks/v1/by-fingerprint/B8B1756A0DDBF0760CE67CCF4ED6CD61932B9EBE#/newsboat.asc; its `Source` line is now that URL (see below)

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | pass |

Tested on 2026-11-05 at dist-git commit `4a30565a89ba` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (verification fails), while `%gpgverify` ignores that. The key owner has updated the key since: the copy at https://keys.openpgp.org/vks/v1/by-fingerprint/B8B1756A0DDBF0760CE67CCF4ED6CD61932B9EBE#/newsboat.asc has the same fingerprint(s) and verifies the release with sqv. This PR replaces the file with that copy, byte for byte, named like the URL, which becomes its `Source`:

```
curl -fsSL -o newsboat.asc 'https://keys.openpgp.org/vks/v1/by-fingerprint/B8B1756A0DDBF0760CE67CCF4ED6CD61932B9EBE'
```

Fingerprints (unchanged):

- `B8B1756A0DDBF0760CE67CCF4ED6CD61932B9EBE`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/newsboat.pgp
+++ upstream/newsboat.pgp
@@ -5,6 +5,5 @@
   Expiration time: 2027-10-17 12:06:26 UTC (creation time + 10years 29days 10h 4m 55s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Newsboat project <newsboat@googlegroups.com>
-self-signatures PositiveCertification: 2017-09-17, 2020-09-20, 2021-09-20, 2022-09-25, 2026-10-04
-self-signatures SubkeyBinding: 2026-10-04
-third-party PositiveCertification: 1
+self-signatures PositiveCertification: 2017-09-17, 2020-09-20, 2021-09-20, 2022-09-25, 2023-09-28, 2025-09-21, 2026-10-04
+self-signatures SubkeyBinding: 2023-09-28, 2025-09-21, 2026-10-04
```

This copy is from keys.openpgp.org, looked up by fingerprint, so it is the same key the old file held. If the project publishes the key somewhere you prefer, that URL works as well, as long as the copy verifies this release. The copy at https://newsboat.org/newsboat.pgp, the old `Source`, expired on 2023-09-25 and does not verify this release.

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is dropped too. To check that nothing else needs it, the changed spec was built completely (`rpmbuild -bb`, including `%check`) in a chroot with gnupg2 and gpgverify removed, and neither the build log nor the test files in the sources mention gpg.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
