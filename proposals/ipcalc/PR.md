# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show ipcalc`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- refreshed keyring `gpgkey-1F42418905D8206AA754CCDC29EE58B996865171.gpg` (see below)

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-12 at dist-git commit `36fa667693d1` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (SHA-1 key self-signatures), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `1F42418905D8206AA754CCDC29EE58B996865171`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/gpgkey-1F42418905D8206AA754CCDC29EE58B996865171.gpg
+++ refreshed/gpgkey-1F42418905D8206AA754CCDC29EE58B996865171.gpg
@@ -1,29 +1,28 @@
       Fingerprint: 1F42418905D8206AA754CCDC29EE58B996865171
-                   Invalid: No binding signature at time 2026-10-12T11:55:26Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2028-04-29 16:35:00 UTC (creation time + 19years 11months 25days 9h 50m 24s)
+        Key flags: certification, signing
            Subkey: 59FBB55CA7F3A8AB0C503773D81C4887F1679A65
-                   Invalid: primary key: No binding signature at time 2026-10-12T11:55:26Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2028-02-04 05:45:13 UTC (creation time + 9years 11months 27days 21h 50m 24s)
+        Key flags: signing
            Subkey: 1F9ABA5E96A1227366ED49A19B4A51263E13AF91
-                   Invalid: primary key: No binding signature at time 2026-10-12T11:55:26Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2028-02-04 05:45:46 UTC (creation time + 9years 11months 27days 21h 50m 24s)
+        Key flags: transport encryption, data-at-rest encryption
            Subkey: A812CBFDFCDC4D0BE7A093129D5EAAF69013B842
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-12T11:55:26Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
            Subkey: 98637A1E80A2414A9D6A7F6AA6B2AEE71404A91D
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-12T11:55:26Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
            UserID: Nikos Mavrogiannopoulos <n.mavrogiannopoulos@gmail.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Nikos Mavrogiannopoulos <nmav@gnutls.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Nikos Mavrogiannopoulos <nmav@hushmail.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2008-05-04, 2008-09-15, 2013-02-25
+                   Revoked:
+self-signatures CertificationRevocation: 2021-02-13
+self-signatures PositiveCertification: 2008-05-04, 2008-09-15, 2013-02-25, 2020-01-09, 2021-02-13
 self-signatures SubkeyBinding: 2008-05-04, 2018-02-06
-third-party CasualCertification: 6
-third-party GenericCertification: 24
+third-party CasualCertification: 7
+third-party GenericCertification: 29
 third-party PersonaCertification: 1
-third-party PositiveCertification: 9
+third-party PositiveCertification: 10
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: the spec has a `%check` section or uses gpg elsewhere, and tests may need it. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
