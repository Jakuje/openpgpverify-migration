# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show lld18`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- refreshed keyring `release-keys.asc` (see below)
- Release bumped (`10%{?dist}` → `11%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-23 at dist-git commit `5748b599f8bc` with sequoia-sqv ? (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `D574BD5D1D0E98895E3BF90044F2485E45D59042`
- `474E22316ABF4785A88C6E8EA2C794A986419D8A`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/release-keys.asc
+++ refreshed/release-keys.asc
@@ -6,13 +6,13 @@
         Key flags: transport encryption, data-at-rest encryption
            UserID: Tobias Hieta <tobias@hieta.se>
       Fingerprint: 474E22316ABF4785A88C6E8EA2C794A986419D8A
-                   Invalid: The primary key is not live: Expired on 2023-05-05T23:33:51Z
-  Expiration time: 2023-05-05 23:33:51 UTC (creation time + 5years 2days 14h 8m 2s)
+                   Invalid: The primary key is not live: Expired on 2026-05-06T21:16:35Z
+  Expiration time: 2026-05-06 21:16:35 UTC (creation time + 8years 3days 17h 50m 46s)
         Key flags: certification, signing
            Subkey: 6717A17756AD71AA42B7E6660AE0D586997F0D1F
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
+                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-05-06T21:16:35Z
+  Expiration time: 2026-05-06 22:13:22 UTC (creation time + 8years 3days 18h 47m 33s)
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Tom Stellard <tstellar@redhat.com>
-self-signatures PositiveCertification: 2018-05-03, 2021-05-05, 2022-08-05
-self-signatures SubkeyBinding: 2018-05-03, 2022-08-05
+self-signatures PositiveCertification: 2018-05-03, 2019-05-02, 2021-05-05, 2022-08-05, 2023-05-17, 2024-05-02, 2025-05-06
+self-signatures SubkeyBinding: 2018-05-03, 2022-08-05, 2023-04-18, 2024-01-13, 2024-05-02, 2025-05-06
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the changed spec does not get past the signature check. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
