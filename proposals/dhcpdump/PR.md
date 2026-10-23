# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show dhcpdump`).

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
- refreshed keyring `signing-key.asc` (see below)
- Release bumped (`1%{?dist}` → `2%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-22 at dist-git commit `9652e38a5ff4` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `BA60BC20F37E59444D6D25001365720913D2F22D`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/signing-key.asc
+++ refreshed/signing-key.asc
@@ -1,13 +1,13 @@
       Fingerprint: BA60BC20F37E59444D6D25001365720913D2F22D
-                   Invalid: The primary key is not live: Expired on 2023-01-30T18:12:31Z
-  Expiration time: 2023-01-30 18:12:31 UTC (creation time + 2years 7months 3days 5h 15m 7s)
+  Expiration time: 2028-07-20 06:06:24 UTC (creation time + 8years 22days 7h 4m 12s)
         Key flags: certification, signing
            Subkey: 5A7BF57ECE76D83A42B1CA620F9A14812426B4F9
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2023-01-30T18:12:31Z
-  Expiration time: 2023-01-30 18:13:04 UTC (creation time + 2years 7months 3days 5h 15m 40s)
+  Expiration time: 2028-07-20 06:07:52 UTC (creation time + 8years 22days 7h 5m 40s)
         Key flags: transport encryption, data-at-rest encryption
+           UserID: Boian Bonev <bbonev@devuan.org>
            UserID: Boian Bonev <bbonev@ipacct.com>
            UserID: Boian Bonev <boian@bonev.com>
            UserID: Boian Bonev <ipacct@gmail.com>
-self-signatures PositiveCertification: 2021-01-30, 2021-02-01
-self-signatures SubkeyBinding: 2021-01-30
+self-signatures PositiveCertification: 2020-06-27, 2021-01-30, 2021-02-01, 2022-07-18, 2022-11-04, 2024-02-10, 2025-01-15, 2026-01-21, 2026-07-21
+self-signatures SubkeyBinding: 2020-06-27, 2021-01-30, 2022-07-18, 2024-02-10, 2025-01-15, 2026-01-21, 2026-07-21
+third-party GenericCertification: 9
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
