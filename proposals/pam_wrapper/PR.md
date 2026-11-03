# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show pam_wrapper`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- dropped `BuildRequires:  gpgverify`, only needed for `%gpgverify`
- rebuilt keyring `pam_wrapper.keyring` from the upstream key at https://cryptomilk.org/0x8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D_asn_cryptomilk_org_gpgkey.asc, completed from keyservers/WKD (see below); the comment above its `Source` line shows the commands

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-12 at dist-git commit `4e1b82165604` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (SHA-1 key self-signatures), while `%gpgverify` ignores that. Upstream publishes the current key at https://cryptomilk.org/0x8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D_asn_cryptomilk_org_gpgkey.asc. That copy has only the latest self-signatures, so it is completed from keyservers/WKD (looked up by fingerprint, WKD; hkps://keys.openpgp.org; hkps://keyserver.ubuntu.com; hkps://sks.pod01.fleetstreetops.com), which have the older self-signatures and subkey bindings that were valid when the release was signed. The keyring is rebuilt from that key, with exactly these commands (also in the comment above the keyring's `Source` line, for the next update):

```
curl -fsSL -o key.asc https://cryptomilk.org/0x8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D_asn_cryptomilk_org_gpgkey.asc
sq --home=none network search --output - 8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D \
  | sq keyring filter --experimental --cert 8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D --output update.pgp
sq keyring merge key.asc update.pgp | sq packet dearmor --output pam_wrapper.keyring.new
mv pam_wrapper.keyring.new pam_wrapper.keyring
rm -f key.asc update.pgp
```

Fingerprints (unchanged):

- `8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/pam_wrapper.keyring
+++ upstream/pam_wrapper.keyring
@@ -1,17 +1,12 @@
       Fingerprint: 8DFF53E18F2ABC8D8F3C92237EE0FC4DCC014E3D
-                   Invalid: No binding signature at time 2026-11-03T09:58:15Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: 9D04ADDA7B3A38E6F9E74DE1668803FBFBA5A04A
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-11-03T09:58:15Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Andreas Schneider <asn@cryptomilk.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Andreas Schneider <asn@redhat.com>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
            UserID: Andreas Schneider <asn@samba.org>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2013-10-05, 2016-03-31
-self-signatures SubkeyBinding: 2013-10-05
+self-signatures PositiveCertification: 2013-10-05, 2016-03-31, 2019-07-16, 2026-10-28
+self-signatures SubkeyBinding: 2013-10-05, 2026-10-28
+third-party CasualCertification: 2
+third-party GenericCertification: 14
+third-party PositiveCertification: 1
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
