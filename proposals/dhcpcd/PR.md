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
- refreshed keyring `rsmarples.gpg` (see below)

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64, fedora-eln-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | pass |

Tested on 2026-11-05 at dist-git commit `051387c2a373` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (verification fails), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR replaces the keyring with the keyserver copy. No key was added or removed. Please check the fingerprint against upstream:

- `A785ED2755955D9E93EA59F6597F97EA9AD45549`

The refresh, as run (the spec comment above the `Source` line has the same command, for the next refresh):

```
sq --home=none network keyserver search A785ED2755955D9E93EA59F6597F97EA9AD45549 --output rsmarples.gpg --overwrite
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/rsmarples.gpg
+++ refreshed/rsmarples.gpg
@@ -1,15 +1,10 @@
       Fingerprint: A785ED2755955D9E93EA59F6597F97EA9AD45549
-                   Invalid: No binding signature at time 2026-11-05T18:18:08Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: E9EE92F5F6D5DBE878B3C2690B0EEE0F057A64CF
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-05T18:18:08Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Roy Marples (NetBSD) <roy@NetBSD.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Roy Marples <roy@marples.name>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2008-11-24, 2008-12-09, 2010-02-20
-self-signatures SubkeyBinding: 2008-11-24
+self-signatures PositiveCertification: 2008-11-24, 2008-12-09, 2010-02-20, 2023-04-24, 2023-04-25
+self-signatures SubkeyBinding: 2008-11-24, 2023-04-24
+third-party CasualCertification: 1
 third-party PositiveCertification: 2
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10. It is not in EPEL 8, so if this spec is still used there, keep `%gpgverify` on that branch.
- `BuildRequires: gnupg2` is dropped too. To check that nothing else needs it, the changed spec was built completely (`rpmbuild -bb`, including `%check`) in a chroot with gnupg2 and gpgverify removed, and neither the build log nor the test files in the sources mention gpg.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
