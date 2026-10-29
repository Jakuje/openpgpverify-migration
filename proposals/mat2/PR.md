# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show mat2`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- refreshed keyring `gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.gpg` (see below); the comment above its `Source` line now shows the commands for refreshing it

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-26 at dist-git commit `70d9a038b8ed` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.mailvelope.com, hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `9FCDEE9E1A381F311EA62A7404D041E8171901CC`

The refresh, as run (the spec comment above the `Source` line has the same commands, for the next refresh):

```
sq --home=none network search --output - 9FCDEE9E1A381F311EA62A7404D041E8171901CC \
  | sq keyring filter --experimental --cert 9FCDEE9E1A381F311EA62A7404D041E8171901CC --output update.pgp
sq keyring merge gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.gpg update.pgp | sq packet dearmor --output gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.gpg.new
mv gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.gpg.new gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.gpg
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.gpg
+++ refreshed/gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.gpg
@@ -1,16 +1,15 @@
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
            UserID: Julien (jvoisin) Voisin <jvoisin@openmailbox.net>
                    Revoked:
-                   Invalid: No binding signature at time 2026-10-27T10:59:29Z
            UserID: Julien (jvoisin) Voisin <jvoisin@riseup.net>
 self-signatures CertificationRevocation: 2016-08-17
-self-signatures PositiveCertification: 2015-07-25, 2015-08-02
-self-signatures SubkeyBinding: 2015-07-25
+self-signatures PositiveCertification: 2015-07-25, 2015-08-02, 2020-04-25, 2020-07-14, 2024-11-08, 2025-04-28, 2025-07-16
+self-signatures SubkeyBinding: 2015-07-25, 2020-07-14, 2025-07-16
+third-party GenericCertification: 6
+third-party PositiveCertification: 2
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the changed spec does not get past the signature check. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
