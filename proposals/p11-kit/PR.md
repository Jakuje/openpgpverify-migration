# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show p11-kit`).

This switches the upstream source signature check from a direct GnuPG call (`gpgv2`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The spec called GnuPG itself instead of using `%gpgverify`; the check becomes one `%openpgpverify` call with the same keyring, signature and data.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- the direct `gpgv2` call is replaced by `%{openpgpverify}` with the same keyring, signature and data
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- refreshed keyring `p11-kit-release-keyring.gpg` (see below)

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`gpgv2`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-26 at dist-git commit `4837e67608d7` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `gpgv2` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `5D46CB0F763405A7053556F47A75A648B3F9220C`
- `462225C3B46F34879FC8496CD605848ED7E69871`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/p11-kit-release-keyring.gpg
+++ refreshed/p11-kit-release-keyring.gpg
@@ -1,25 +1,20 @@
       Fingerprint: 5D46CB0F763405A7053556F47A75A648B3F9220C
-                   Invalid: The primary key is not live: Expired on 2023-12-23T11:16:51Z
-  Expiration time: 2023-12-23 11:16:51 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2027-09-18 12:46:25 UTC (creation time + 5years 8months 25days 7h 46s)
         Key flags: certification, signing
            Subkey: DF7B507669E926A2A1F09BBB46CFDAE328F33704
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2023-12-23T11:16:51Z
-  Expiration time: 2023-12-23 11:16:51 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2027-01-01 13:13:03 UTC (creation time + 5years 8days 19h 56m 12s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Zoltan Fridrich <zfridric@redhat.com>
       Fingerprint: 462225C3B46F34879FC8496CD605848ED7E69871
-                   Invalid: No binding signature at time 2026-10-26T20:12:18Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2027-10-17 02:52:01 UTC (creation time + 18years 2months 24days 12h 45m 23s)
+        Key flags: certification, signing
            Subkey: 2567E23B4A79AD4DC685099850AD4600C8C530D6
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-26T20:12:18Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Daiki Ueno <ueno@gnu.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Daiki Ueno <ueno@unixuser.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2009-07-23, 2018-09-26, 2021-12-23
-self-signatures SubkeyBinding: 2010-02-04, 2021-12-23
-third-party GenericCertification: 8
+self-signatures PositiveCertification: 2009-07-23, 2012-12-25, 2013-10-05, 2013-10-06, 2018-09-26, 2021-12-23, 2023-06-30, 2024-01-02, 2025-09-18, 2026-10-17
+self-signatures SubkeyBinding: 2010-02-04, 2021-12-23, 2023-07-03, 2024-01-02
+third-party CasualCertification: 1
+third-party CertificationRevocation: 1
+third-party GenericCertification: 11
 third-party PositiveCertification: 1
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the changed spec does not get past the signature check. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
