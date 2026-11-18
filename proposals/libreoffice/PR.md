# Verify source signatures with openpgpverify

This switches the upstream source signature check from direct GnuPG calls (`gpg2`, `gpgv2`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The spec called GnuPG itself instead of using `%gpgverify`; each of the three checks becomes one `%openpgpverify` call with the same key, signature and data.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- the GnuPG verification (`gpg2 --dearmor` of the armored key into a temporary keyring, then three `gpgv2` calls) is replaced by three `%{openpgpverify}` calls with the same key, signatures and data; sqv reads the armored key file directly
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- `BuildRequires: gnupg2` stays; the package has `%check` and builds against gpgme, and I could not check whether the build or the tests need it (see below). If you know they don't, it can go.

### Testing

The sources are too large for my test machine to run the usual `rpmbuild -bp` comparison in mock, so this PR was not test-built; the CI build of this PR is the real test. What was checked:

- The three tarballs and their signatures from the lookaside cache (dist-git commit `6b43b39e3e1c`, 26.8.3.1) verify with `sqv` against `gpgkey-C2839ECAD9408FBE9531C3E9F434A1EFAFEEAEA3.gpg.asc`, exactly as the new `%openpgpverify` calls do (sequoia-sqv 1.5.0-1.fc44.x86_64, Fedora DEFAULT crypto policy).
- The spec change itself is mechanical and the same as in the other converted packages.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
