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
- updated `pgp.asc` to the current upstream copy from the URL in the spec (see below)

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64, fedora-eln-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | pass |

Tested on 2026-11-16 at dist-git commit `e4699268cb9b` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (SHA-1 key self-signatures), while `%gpgverify` ignores that. Upstream has updated the key since: the copy at https://www.stunnel.org/pgp.asc has the same fingerprint(s) and verifies the release with sqv. This PR replaces the file with that copy, byte for byte:

```
curl -fsSL -o pgp.asc https://www.stunnel.org/pgp.asc
```

Fingerprints (unchanged):

- `AC915EA30645D9D3D4DAE4FEB1048932DD3AAAA3`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/pgp.asc
+++ upstream/pgp.asc
@@ -1,16 +1,13 @@
       Fingerprint: AC915EA30645D9D3D4DAE4FEB1048932DD3AAAA3
         Key flags: certification, signing
-           Subkey: 19FFB7E9CA02BF4B6C464AA2970387EEC478CB9A
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
            Subkey: 2BC7E4E67E3CC0C1BEA72F8C2EFC7FF0D416E014
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
+        Key flags: signing
+           Subkey: 19FFB7E9CA02BF4B6C464AA2970387EEC478CB9A
+        Key flags: transport encryption, data-at-rest encryption
            UserID: Michał Trojnara (auxiliary address) <Michal.Trojnara@gmail.com>
            UserID: Michał Trojnara <Michal.Trojnara@mirt.net>
            UserID: Michał Trojnara <Michal.Trojnara@mobi-com.net>
            UserID: Michał Trojnara <Michal.Trojnara@stunnel.org>
-self-signatures PositiveCertification: 2022-05-10
+self-signatures PositiveCertification: 2015-02-06, 2022-05-10
 self-signatures SubkeyBinding: 2015-02-06
+third-party GenericCertification: 1
```

This fixes [rhbz#2569342](https://bugzilla.redhat.com/show_bug.cgi?id=2569342), filed for the failing check.

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is dropped too. To check that nothing else needs it, the changed spec was built completely (`rpmbuild -bb`, including `%check`) in a chroot with gnupg2 and gpgverify removed, and neither the build log nor the test files in the sources mention gpg.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
