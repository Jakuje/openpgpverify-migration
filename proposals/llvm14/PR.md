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
- dropped `BuildRequires:	gnupg2`, only needed for `%gpgverify`
- refreshed keyring `tstellar-gpg-key.asc` (see below)
- Release bumped (`15%{?dist}` → `16%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64, fedora-eln-x86_64, where even the current spec cannot install its build dependencies). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | pass |

Tested on 2026-11-06 at dist-git commit `24d7b953e613` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (verification fails), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR replaces the keyring with the keyserver copy. No key was added or removed. Please check the fingerprint against upstream:

- `474E22316ABF4785A88C6E8EA2C794A986419D8A`

The refresh, as run (the spec comment above the `Source` line has the same command, for the next refresh):

```
sq --home=none network keyserver search 474E22316ABF4785A88C6E8EA2C794A986419D8A --output tstellar-gpg-key.asc --overwrite
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/tstellar-gpg-key.asc
+++ refreshed/tstellar-gpg-key.asc
@@ -1,11 +1,11 @@
       Fingerprint: 474E22316ABF4785A88C6E8EA2C794A986419D8A
-                   Invalid: No binding signature at time 2026-11-05T18:19:38Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: The primary key is not live: Expired on 2026-05-06T21:16:35Z
+  Expiration time: 2026-05-06 21:16:35 UTC (creation time + 8years 3days 17h 50m 46s)
+        Key flags: certification, signing
            Subkey: 6717A17756AD71AA42B7E6660AE0D586997F0D1F
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-05T18:19:38Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-05-06T21:16:35Z
+  Expiration time: 2026-05-06 22:13:22 UTC (creation time + 8years 3days 18h 47m 33s)
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Tom Stellard <tstellar@redhat.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2018-05-03
-self-signatures SubkeyBinding: 2018-05-03
+self-signatures PositiveCertification: 2018-05-03, 2019-05-02, 2021-05-05, 2023-05-17, 2024-05-02, 2025-05-06
+self-signatures SubkeyBinding: 2018-05-03, 2023-04-18, 2024-01-13, 2024-05-02, 2025-05-06
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is dropped too, without a full build: the sources are too large for the test machine. Nothing in the spec uses gpg besides the signature check. If the build turns out to need it, it can come back.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
