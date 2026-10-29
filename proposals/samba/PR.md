# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show samba`).

This switches the upstream source signature check from a direct GnuPG call (`gpgv2`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The spec called GnuPG itself instead of using `%gpgverify`; the check becomes one `%openpgpverify` call with the same keyring, signature and data.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- the direct `gpgv2` call is replaced by `%{openpgpverify}` with the same keyring, signature and data
- `%gpgverify` → `%openpgpverify` for the existing macro call
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- refreshed keyring `samba-pubkey_AA99442FB680B620.gpg` (see below); the comment above its `Source` line now shows the commands for refreshing it

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`gpgv2`) | 2 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-26 at dist-git commit `0e3f8ac9c02a` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `gpgv2` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `81F5E2832BD2545A1897B713AA99442FB680B620`

The refresh, as run (the spec comment above the `Source` line has the same commands, for the next refresh):

```
sq --home=none network search --output - 81F5E2832BD2545A1897B713AA99442FB680B620 \
  | sq keyring filter --experimental --cert 81F5E2832BD2545A1897B713AA99442FB680B620 --output update.pgp
sq keyring merge samba-pubkey_AA99442FB680B620.gpg update.pgp | sq packet dearmor --output samba-pubkey_AA99442FB680B620.gpg.new
mv samba-pubkey_AA99442FB680B620.gpg.new samba-pubkey_AA99442FB680B620.gpg
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/samba-pubkey_AA99442FB680B620.gpg
+++ refreshed/samba-pubkey_AA99442FB680B620.gpg
@@ -1,11 +1,10 @@
       Fingerprint: 81F5E2832BD2545A1897B713AA99442FB680B620
-                   Invalid: The primary key is not live: Expired on 2022-12-21T12:11:00Z
-  Expiration time: 2022-12-21 12:11:00 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2027-12-12 17:06:40 UTC (creation time + 6years 11months 20days 20h 46m 4s)
         Key flags: certification, signing
            Subkey: 8ECB3E1AD3C66464249027DE97EF9386FBFD4002
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-12-21T12:11:00Z
-  Expiration time: 2022-12-21 12:11:00 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2027-12-12 17:09:32 UTC (creation time + 6years 11months 20days 20h 48m 56s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Samba Distribution Verification Key <samba-bugs@samba.org>
-self-signatures PositiveCertification: 2020-12-21
-self-signatures SubkeyBinding: 2020-12-21
+self-signatures PositiveCertification: 2020-12-21, 2022-12-19, 2023-12-18, 2024-10-15, 2025-12-12
+self-signatures SubkeyBinding: 2020-12-21, 2022-12-19, 2023-12-18, 2024-10-15, 2025-12-12
+third-party GenericCertification: 1
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10. It is not in EPEL 8, so if this spec is still used there, keep `%gpgverify` on that branch.
- `BuildRequires: gnupg2` is kept: the spec has a `%check` section or uses gpg elsewhere, and tests may need it. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
