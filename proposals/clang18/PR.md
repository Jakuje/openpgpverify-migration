# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show clang18`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (2 calls; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- updated `release-keys.asc` to the current upstream copy from the URL in the spec (see below)
- Release bumped (`11%{?dist}` → `12%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 2 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-26 at dist-git commit `4aea9b4819d2` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. Upstream has updated the key since: the copy at https://releases.llvm.org/release-keys.asc has the same fingerprint(s) and also holds other keys upstream publishes there and verifies the release with sqv. This PR replaces the file with that copy, byte for byte:

```
curl -fsSL -O https://releases.llvm.org/release-keys.asc
```

Fingerprints (unchanged):

- `D574BD5D1D0E98895E3BF90044F2485E45D59042`
- `474E22316ABF4785A88C6E8EA2C794A986419D8A`

Added to the keyring, because upstream's file holds them too; this also means a release signed with one of them will verify:

- `B6C8F98282B944E3B0D5C2530FC3042E345AD05D`
- `0FB96824606D15FDD54C3D092FFC629D3F563BDC`
- `71046D1E9C6656BDD61171873E83BABF4A4F9E85`
- `FFB3368980F3E6BB5737145A316C56D064CACBA5`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/release-keys.asc
+++ upstream/release-keys.asc
@@ -6,13 +6,39 @@
         Key flags: transport encryption, data-at-rest encryption
            UserID: Tobias Hieta <tobias@hieta.se>
       Fingerprint: 474E22316ABF4785A88C6E8EA2C794A986419D8A
-                   Invalid: The primary key is not live: Expired on 2023-05-05T23:33:51Z
-  Expiration time: 2023-05-05 23:33:51 UTC (creation time + 5years 2days 14h 8m 2s)
+                   Invalid: The primary key is not live: Expired on 2025-05-02T17:49:59Z
+  Expiration time: 2025-05-02 17:49:59 UTC (creation time + 6years 11months 30days 6h 14m 34s)
         Key flags: certification, signing
            Subkey: 6717A17756AD71AA42B7E6660AE0D586997F0D1F
+                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-05-02T17:49:59Z
+  Expiration time: 2025-05-02 17:51:32 UTC (creation time + 6years 11months 30days 6h 16m 7s)
+        Key flags: transport encryption, data-at-rest encryption
+           UserID: Tom Stellard <tstellar@redhat.com>
+      Fingerprint: B6C8F98282B944E3B0D5C2530FC3042E345AD05D
+  Expiration time: 2029-10-15 09:20:01 UTC (creation time + 14years 8months 24days 10h 28m 49s)
+        Key flags: certification, signing
+           Subkey: A7F1C1CD2428B2B66C09AD8E3276ABBAE8E36D78
+  Expiration time: 2029-10-15 09:20:55 UTC (creation time + 10years 6months 11days 21h 8m 23s)
+        Key flags: transport encryption, data-at-rest encryption
+           Subkey: C569F42EE903DB0A0AB4B1768514EA9C9330FC0D
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
-           UserID: Tom Stellard <tstellar@redhat.com>
-self-signatures PositiveCertification: 2018-05-03, 2021-05-05, 2022-08-05
-self-signatures SubkeyBinding: 2018-05-03, 2022-08-05
+           UserID: Hans Wennborg <hans@chromium.org>
+      Fingerprint: 0FB96824606D15FDD54C3D092FFC629D3F563BDC
+        Key flags: certification, signing
+           Subkey: 295E95E904B8FFCE900EF7B2256F54DAEDBE640D
+        Key flags: transport encryption, data-at-rest encryption
+           UserID: Muhammad Omair Javaid (LLVM Release Signing Key) <omair.javaid@linaro.org>
+      Fingerprint: 71046D1E9C6656BDD61171873E83BABF4A4F9E85
+        Key flags: certification, signing
+           Subkey: FC375C4C3D0910B7856F6FD8DB76C32D7B72878B
+        Key flags: transport encryption, data-at-rest encryption
+           UserID: Cullen Rhodes <cullen.rhodes@arm.com>
+      Fingerprint: FFB3368980F3E6BB5737145A316C56D064CACBA5
+        Key flags: certification, signing
+           Subkey: 1FE1C822C37D38862D36BBE9B977855DC9580AA9
+        Key flags: transport encryption, data-at-rest encryption
+           UserID: Douglas Yung <douglas.yung@sony.com>
+self-signatures PositiveCertification: 2018-05-03, 2022-08-05, 2024-05-02, 2024-10-15, 2024-10-16, 2025-09-15
+self-signatures SubkeyBinding: 2018-01-16, 2022-08-05, 2024-05-02, 2024-10-15, 2024-10-16, 2025-09-15
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the changed spec does not get past the signature check. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
