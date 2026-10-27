# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show rpki-client`).

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
- updated `B5B6416FEA6DDA05EA562A9FCB987F2783972FF9` to the current upstream copy from the URL in the spec (see below)
- Release bumped (`1%{?with_snapshot:.git%{gitdate}}%{?dist}` → `2%{?with_snapshot:.git%{gitdate}}%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-23 at dist-git commit `361aac0b05d3` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. Upstream has updated the key since: the copy at the URL the spec names for it has the same fingerprint(s) and verifies the release with sqv. This PR replaces the file with that copy, byte for byte:

```
curl -fsSL -o B5B6416FEA6DDA05EA562A9FCB987F2783972FF9 https://keys.openpgp.org/vks/v1/by-fingerprint/B5B6416FEA6DDA05EA562A9FCB987F2783972FF9
```

Fingerprints (unchanged):

- `B5B6416FEA6DDA05EA562A9FCB987F2783972FF9`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/B5B6416FEA6DDA05EA562A9FCB987F2783972FF9
+++ upstream/B5B6416FEA6DDA05EA562A9FCB987F2783972FF9
@@ -1,6 +1,5 @@
       Fingerprint: B5B6416FEA6DDA05EA562A9FCB987F2783972FF9
-                   Invalid: The primary key is not live: Expired on 2026-03-18T18:43:06Z
-  Expiration time: 2026-03-18 18:43:06 UTC (creation time + 5years 11months 3days 18h 38m 33s)
+  Expiration time: 2028-04-13 19:57:07 UTC (creation time + 7years 11months 30days 7h 52m 34s)
         Key flags: certification, signing
            UserID: Sebastian Benoit (software signing only) <benno@openbsd.org>
-self-signatures PositiveCertification: 2023-03-19
+self-signatures PositiveCertification: 2021-04-15, 2023-03-19, 2026-04-14
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the changed spec does not get past the signature check. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
