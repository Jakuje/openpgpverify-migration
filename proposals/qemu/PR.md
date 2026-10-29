# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show qemu`).

This switches the upstream source signature check from a direct GnuPG call (`gpgv2`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The spec called GnuPG itself instead of using `%gpgverify`; the check becomes one `%openpgpverify` call with the same keyring, signature and data.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- the direct `gpgv2` call is replaced by `%{openpgpverify}` with the same keyring, signature and data
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- refreshed keyring `gpgkey-CEACC9E15534EBABB82D3FA03353C9CEF108B584.gpg` (see below); the comment above its `Source` line now shows the commands for refreshing it

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`gpgv2`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-26 at dist-git commit `81d8c3689b0a` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (SHA-1 key self-signatures), while `gpgv2` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `CEACC9E15534EBABB82D3FA03353C9CEF108B584`

The refresh, as run (the spec comment above the `Source` line has the same commands, for the next refresh):

```
sq --home=none network search --output - CEACC9E15534EBABB82D3FA03353C9CEF108B584 \
  | sq keyring filter --experimental --cert CEACC9E15534EBABB82D3FA03353C9CEF108B584 --output update.pgp
sq keyring merge gpgkey-CEACC9E15534EBABB82D3FA03353C9CEF108B584.gpg update.pgp | sq packet dearmor --output gpgkey-CEACC9E15534EBABB82D3FA03353C9CEF108B584.gpg.new
mv gpgkey-CEACC9E15534EBABB82D3FA03353C9CEF108B584.gpg.new gpgkey-CEACC9E15534EBABB82D3FA03353C9CEF108B584.gpg
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/gpgkey-CEACC9E15534EBABB82D3FA03353C9CEF108B584.gpg
+++ refreshed/gpgkey-CEACC9E15534EBABB82D3FA03353C9CEF108B584.gpg
@@ -1,17 +1,21 @@
       Fingerprint: CEACC9E15534EBABB82D3FA03353C9CEF108B584
-                   Invalid: No binding signature at time 2026-10-27T11:04:25Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2031-05-26 21:02:33 UTC (creation time + 17years 7months 6days 22h 58m 2s)
+        Key flags: certification, signing
            Subkey: B771E2672C6A23D7CC3CD7643B0B7D75D7AC684E
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-27T11:04:25Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
            UserID: Michael Roth <flukshun@gmail.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Michael Roth <mdroth@linux.vnet.ibm.com>
+                   Revoked:
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
            UserID: Michael Roth <mdroth@utexas.edu>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2013-10-18
+           UserID: Michael Roth <michael.roth@amd.com>
+self-signatures CertificationRevocation: 2020-10-27
+self-signatures PositiveCertification: 2013-10-18, 2020-10-27, 2024-05-11, 2026-05-27
 self-signatures SubkeyBinding: 2013-10-18
+third-party CasualCertification: 2
+third-party GenericCertification: 8
+third-party PersonaCertification: 2
+third-party PositiveCertification: 2
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: sources over 40 MB, too large for the full build without gnupg2 on the test machine. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
