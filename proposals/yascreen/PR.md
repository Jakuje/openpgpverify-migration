# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show yascreen`).

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
- updated `signing-key.asc` to the current upstream copy from the URL in the spec (see below)
- Release bumped (`1%{?dist}` → `2%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-22 at dist-git commit `72b65d632505` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. Upstream has updated the key since: the copy at the URL the spec names for it has the same fingerprint(s) and verifies the release with sqv. This PR replaces the file with that copy, byte for byte:

```
curl -fsSL -o signing-key.asc https://raw.githubusercontent.com/bbonev/yascreen/master/debian/upstream/signing-key.asc
```

Fingerprints (unchanged):

- `BA60BC20F37E59444D6D25001365720913D2F22D`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/signing-key.asc
+++ upstream/signing-key.asc
@@ -1,13 +1,12 @@
       Fingerprint: BA60BC20F37E59444D6D25001365720913D2F22D
-                   Invalid: The primary key is not live: Expired on 2023-01-30T18:12:31Z
-  Expiration time: 2023-01-30 18:12:31 UTC (creation time + 2years 7months 3days 5h 15m 7s)
+  Expiration time: 2028-01-21 06:00:35 UTC (creation time + 7years 6months 23days 21h 36m 47s)
         Key flags: certification, signing
            Subkey: 5A7BF57ECE76D83A42B1CA620F9A14812426B4F9
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2023-01-30T18:12:31Z
-  Expiration time: 2023-01-30 18:13:04 UTC (creation time + 2years 7months 3days 5h 15m 40s)
+  Expiration time: 2028-01-21 06:00:17 UTC (creation time + 7years 6months 23days 21h 36m 29s)
         Key flags: transport encryption, data-at-rest encryption
+           UserID: Boian Bonev <bbonev@devuan.org>
            UserID: Boian Bonev <bbonev@ipacct.com>
            UserID: Boian Bonev <boian@bonev.com>
            UserID: Boian Bonev <ipacct@gmail.com>
-self-signatures PositiveCertification: 2020-06-27, 2021-01-30, 2021-02-01
-self-signatures SubkeyBinding: 2020-06-27, 2021-01-30
+self-signatures PositiveCertification: 2026-01-21
+self-signatures SubkeyBinding: 2026-01-21
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
