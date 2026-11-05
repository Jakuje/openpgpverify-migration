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
- replaced keyring `gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.gpg` with `gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.asc` from https://keys.openpgp.org/vks/v1/by-fingerprint/9FCDEE9E1A381F311EA62A7404D041E8171901CC#/gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.asc; its `Source` line is now that URL (see below)

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | pass |

Tested on 2026-11-05 at dist-git commit `70d9a038b8ed` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (verification fails), while `%gpgverify` ignores that. The key owner has updated the key since: the copy at https://keys.openpgp.org/vks/v1/by-fingerprint/9FCDEE9E1A381F311EA62A7404D041E8171901CC#/gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.asc has the same fingerprint(s) and verifies the release with sqv. This PR replaces the file with that copy, byte for byte, named like the URL, which becomes its `Source`:

```
curl -fsSL -o gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.asc 'https://keys.openpgp.org/vks/v1/by-fingerprint/9FCDEE9E1A381F311EA62A7404D041E8171901CC'
```

Fingerprints (unchanged):

- `9FCDEE9E1A381F311EA62A7404D041E8171901CC`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.gpg
+++ upstream/gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.gpg
@@ -1,16 +1,10 @@
       Fingerprint: 9FCDEE9E1A381F311EA62A7404D041E8171901CC
-                   Invalid: The primary key is not live: Expired on 2020-07-23T17:21:36Z
-  Expiration time: 2020-07-23 17:21:36 UTC (creation time + 4years 11months 29days 3h 50m 24s)
+  Expiration time: 2030-07-15 22:00:00 UTC (creation time + 14years 11months 20days 20h 28m 48s)
         Key flags: certification, signing
            Subkey: 0CB250E28DD3BB8EFA4553E4AC28F00D0351B960
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2020-07-23T17:21:36Z
-  Expiration time: 2020-07-23 17:21:36 UTC (creation time + 4years 11months 29days 3h 50m 24s)
+  Expiration time: 2030-07-15 22:00:00 UTC (creation time + 14years 11months 20days 20h 28m 48s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Julien (jvoisin) Voisin <julien.voisin@dustri.org>
-           UserID: Julien (jvoisin) Voisin <jvoisin@openmailbox.net>
-                   Revoked:
-                   Invalid: No binding signature at time 2026-11-05T09:38:28Z
            UserID: Julien (jvoisin) Voisin <jvoisin@riseup.net>
-self-signatures CertificationRevocation: 2016-08-17
-self-signatures PositiveCertification: 2015-07-25, 2015-08-02
-self-signatures SubkeyBinding: 2015-07-25
+self-signatures PositiveCertification: 2015-07-25, 2015-08-02, 2020-04-25, 2020-07-14, 2024-11-08, 2025-04-28, 2025-07-16
+self-signatures SubkeyBinding: 2015-07-25, 2020-07-14, 2025-07-16
```

This copy is from keys.openpgp.org, looked up by fingerprint, so it is the same key the old file held. If the project publishes the key somewhere you prefer, that URL works as well, as long as the copy verifies this release.

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the build fails with gnupg2 too (rc 1). If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
