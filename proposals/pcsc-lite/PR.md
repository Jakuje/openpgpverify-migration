# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show pcsc-lite`).

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
- refreshed keyring `gpgkey-F5E11B9FFE911146F41D953D78A1B4DFE8F9C57E.gpg` (see below)

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-12 at dist-git commit `67d3c51d8c3d` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (SHA-1 key self-signatures), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `F5E11B9FFE911146F41D953D78A1B4DFE8F9C57E`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/gpgkey-F5E11B9FFE911146F41D953D78A1B4DFE8F9C57E.gpg
+++ refreshed/gpgkey-F5E11B9FFE911146F41D953D78A1B4DFE8F9C57E.gpg
@@ -1,18 +1,19 @@
       Fingerprint: F5E11B9FFE911146F41D953D78A1B4DFE8F9C57E
-                   Invalid: No binding signature at time 2026-10-12T11:56:53Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: 1FB866BC68EFCC584B1A974B2533629C5982E499
-                   Invalid: primary key: No binding signature at time 2026-10-12T11:56:53Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: The subkey is not live: Expired on 2012-12-03T16:19:52Z
+  Expiration time: 2012-12-03 16:19:52 UTC (creation time + 11months 30days 3h 50m 24s)
+        Key flags: signing
            Subkey: AF1912CE1D685FF5ACF7C26E36A241532F1BEFF0
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-12T11:56:53Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: transport encryption, data-at-rest encryption
+           Subkey: 2C7657A42E6C6465E14CD591A782179B0F37B7F7
+                   Invalid: The subkey is not live: Expired on 2016-02-19T14:14:14Z
+  Expiration time: 2016-02-19 14:14:14 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Ludovic Rousseau <ludovic.rousseau@free.fr>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Ludovic Rousseau <rousseau@debian.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2010-09-19
-self-signatures SubkeyBinding: 2010-09-19, 2011-12-04
-third-party GenericCertification: 4
+self-signatures PositiveCertification: 2010-09-19, 2025-03-20
+self-signatures SubkeyBinding: 2010-09-19, 2011-12-04, 2014-02-19, 2025-03-20
+third-party CasualCertification: 2
+third-party GenericCertification: 8
 third-party PositiveCertification: 3
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
