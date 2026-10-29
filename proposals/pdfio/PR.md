# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show pdfio`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- dropped `BuildRequires: gpgverify`, only needed for `%gpgverify`
- refreshed keyring `msweet-pub.gpg` (see below); the comment above its `Source` line now shows the commands for refreshing it
- Release bumped (`1%{?dist}` → `2%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-12 at dist-git commit `ade398c26602` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `9086C3CDC66C3F563CF8F405BE67C75EC81F3244`

The refresh, as run (the spec comment above the `Source` line has the same commands, for the next refresh):

```
sq --home=none network search --output - 9086C3CDC66C3F563CF8F405BE67C75EC81F3244 \
  | sq keyring filter --experimental --cert 9086C3CDC66C3F563CF8F405BE67C75EC81F3244 --output update.pgp
sq keyring merge --output msweet-pub.gpg.new msweet-pub.gpg update.pgp
mv msweet-pub.gpg.new msweet-pub.gpg
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/msweet-pub.gpg
+++ refreshed/msweet-pub.gpg
@@ -1,11 +1,9 @@
       Fingerprint: 9086C3CDC66C3F563CF8F405BE67C75EC81F3244
-                   Invalid: The primary key is not live: Expired on 2024-10-30T22:06:43Z
-  Expiration time: 2024-10-30 22:06:43 UTC (creation time + 4years)
+  Expiration time: 2029-11-01 19:05:45 UTC (creation time + 9years 1day 14h 59m 2s)
         Key flags: certification, signing
            Subkey: C53DB51FF598C6F84B524FBEA692FD1B4D815AE0
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2024-10-30T22:06:43Z
-  Expiration time: 2024-10-30 22:06:43 UTC (creation time + 4years)
+  Expiration time: 2026-11-01 20:05:46 UTC (creation time + 6years 1day 9h 59m 3s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Michael R Sweet <msweet@msweet.org>
-self-signatures PositiveCertification: 2020-10-30
-self-signatures SubkeyBinding: 2020-10-30
+self-signatures PositiveCertification: 2020-10-30, 2024-11-01, 2025-11-11
+self-signatures SubkeyBinding: 2020-10-30, 2024-11-01
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
