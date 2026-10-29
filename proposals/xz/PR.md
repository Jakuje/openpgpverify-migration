# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show xz`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- updated `lasse_collin_pubkey.txt` to the current upstream copy from the URL in the spec (see below)
- Release bumped (`1%{?dist}` → `2%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-12 at dist-git commit `9624ab456837` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. Upstream has updated the key since: the copy at the URL the spec names for it has the same fingerprint(s) and verifies the release with sqv. This PR replaces the file with that copy, byte for byte:

```
curl -fsSL -o lasse_collin_pubkey.txt https://tukaani.org/misc/lasse_collin_pubkey.txt
```

Fingerprints (unchanged):

- `3690C240CE51B4670D30AD1C38EE757D69184620`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/lasse_collin_pubkey.txt
+++ upstream/lasse_collin_pubkey.txt
@@ -1,11 +1,9 @@
       Fingerprint: 3690C240CE51B4670D30AD1C38EE757D69184620
-                   Invalid: The primary key is not live: Expired on 2025-02-07T14:42:17Z
-  Expiration time: 2025-02-07 14:42:17 UTC (creation time + 14years 3months 15days 5h 11m 19s)
+  Expiration time: 2027-02-10 10:00:01 UTC (creation time + 16years 3months 17days 12h 29m 3s)
         Key flags: certification, signing
            Subkey: 06D04A6B37AF445DABE0D6DA5923A9D358ADF744
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-02-07T14:42:17Z
-  Expiration time: 2025-02-07 14:41:54 UTC (creation time + 14years 3months 15days 5h 10m 56s)
+  Expiration time: 2027-02-10 10:00:06 UTC (creation time + 16years 3months 17days 12h 29m 8s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Lasse Collin <lasse.collin@tukaani.org>
-self-signatures PositiveCertification: 2024-01-08
-self-signatures SubkeyBinding: 2024-01-08
+self-signatures PositiveCertification: 2026-01-16
+self-signatures SubkeyBinding: 2026-01-16
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: the spec has a `%check` section or uses gpg elsewhere, and tests may need it. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
