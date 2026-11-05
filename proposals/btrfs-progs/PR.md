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
- dropped `BuildRequires:  gnupg2`, only needed for `%gpgverify`
- replaced keyring `gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg` with `C565D5F9D76D583B.asc` from https://git.kernel.org/pub/scm/docs/kernel/pgpkeys.git/plain/keys/C565D5F9D76D583B.asc; its `Source` line is now that URL (see below)
- Release bumped (`3%{?dist}` → `4%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64, fedora-eln-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | pass |

Tested on 2026-11-05 at dist-git commit `35030463c68f` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (verification fails), while `%gpgverify` ignores that. Upstream has updated the key since: the copy at https://git.kernel.org/pub/scm/docs/kernel/pgpkeys.git/plain/keys/C565D5F9D76D583B.asc has the same fingerprint(s) and verifies the release with sqv. This PR replaces the file with that copy, byte for byte, named like the URL, which becomes its `Source`:

```
curl -fsSL -O https://git.kernel.org/pub/scm/docs/kernel/pgpkeys.git/plain/keys/C565D5F9D76D583B.asc
```

Fingerprints (unchanged):

- `F2B41200C54EFB30380C1756C565D5F9D76D583B`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg
+++ upstream/gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg
@@ -1,13 +1,12 @@
       Fingerprint: F2B41200C54EFB30380C1756C565D5F9D76D583B
-                   Invalid: The primary key is not live: Expired on 2024-08-24T18:40:54Z
-  Expiration time: 2024-08-24 18:40:54 UTC (creation time + 9years 11months 27days 21h 50m 24s)
+  Expiration time: 2034-01-09 00:19:59 UTC (creation time + 19years 4months 12days 17h 24m 41s)
         Key flags: certification, signing
            Subkey: 4421024497B071710005477564AE64A9A61BB5A1
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2024-08-24T18:40:54Z
         Key flags: transport encryption, data-at-rest encryption
            UserID: David Sterba <dave@jikos.cz>
            UserID: David Sterba <dsterba@suse.com>
            UserID: David Sterba <dsterba@suse.cz>
            UserID: David Sterba <kdave@kernel.org>
-self-signatures PositiveCertification: 2014-08-27, 2014-09-12
+self-signatures PositiveCertification: 2024-01-12
 self-signatures SubkeyBinding: 2014-08-27
+third-party PositiveCertification: 1
```

The URL is the pgpkeys repository of kernel.org. Browsers may get an anti-bot page there; curl and spectool get the key file.

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is dropped too. To check that nothing else needs it, the changed spec was built completely (`rpmbuild -bb`; the spec has no `%check`) in a chroot with gnupg2 and gpgverify removed, and the build log doesn't mention gpg.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
