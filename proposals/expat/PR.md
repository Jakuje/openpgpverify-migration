# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show expat`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- updated `3176EF7DB2367F1FCA4F306B1F9B0E909AF37285` to the current upstream copy from the URL in the spec (see below)

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-12 at dist-git commit `31e641b11f28` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. Upstream has updated the key since: the copy at the URL the spec names for it has the same fingerprint(s) and verifies the release with sqv. This PR replaces the file with that copy, byte for byte:

```
curl -fsSL -o 3176EF7DB2367F1FCA4F306B1F9B0E909AF37285 https://keys.openpgp.org/vks/v1/by-fingerprint/3176EF7DB2367F1FCA4F306B1F9B0E909AF37285
```

Fingerprints (unchanged):

- `3176EF7DB2367F1FCA4F306B1F9B0E909AF37285`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/3176EF7DB2367F1FCA4F306B1F9B0E909AF37285
+++ upstream/3176EF7DB2367F1FCA4F306B1F9B0E909AF37285
@@ -1,15 +1,12 @@
       Fingerprint: 3176EF7DB2367F1FCA4F306B1F9B0E909AF37285
-                   Invalid: The primary key is not live: Expired on 2026-01-04T15:35:59Z
-  Expiration time: 2026-01-04 15:35:59 UTC (creation time + 6years 7months 27days 7h 16m 34s)
+  Expiration time: 2026-12-28 19:31:59 UTC (creation time + 7years 7months 20days 5h 12m 34s)
         Key flags: certification, signing
            Subkey: CB8DE70A90CFBF6C3BF5CC5696262ACFFBD3AEC6
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-01-04T15:35:59Z
-  Expiration time: 2026-01-04 15:36:42 UTC (creation time + 6years 7months 27days 7h 8m 45s)
+  Expiration time: 2026-12-28 19:32:44 UTC (creation time + 7years 7months 20days 5h 4m 47s)
         Key flags: signing
            Subkey: A10DAC3EE122F79957D65403BF9802AEE9F129C3
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-01-04T15:35:59Z
-  Expiration time: 2026-01-04 15:36:42 UTC (creation time + 6years 7months 27days 7h 17m 17s)
+  Expiration time: 2026-12-28 19:32:44 UTC (creation time + 7years 7months 20days 5h 13m 19s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Sebastian Pipping <sping@gentoo.org>
-self-signatures PositiveCertification: 2019-05-09, 2022-01-02, 2023-01-17, 2024-01-05
-self-signatures SubkeyBinding: 2019-05-09, 2022-01-02, 2023-01-17, 2024-01-05
+self-signatures PositiveCertification: 2019-05-09, 2022-01-02, 2023-01-17, 2024-01-05, 2025-12-28
+self-signatures SubkeyBinding: 2019-05-09, 2022-01-02, 2023-01-17, 2024-01-05, 2025-12-28
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: the spec has a `%check` section or uses gpg elsewhere, and tests may need it. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
