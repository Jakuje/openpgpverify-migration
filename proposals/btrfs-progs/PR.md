# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show btrfs-progs`).

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
- refreshed keyring `gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg` (see below); the comment above its `Source` line now shows the commands for refreshing it
- Release bumped (`3%{?dist}` → `4%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-26 at dist-git commit `35030463c68f` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `F2B41200C54EFB30380C1756C565D5F9D76D583B`

The refresh, as run (the spec comment above the `Source` line has the same commands, for the next refresh):

```
sq --home=none network search --output - F2B41200C54EFB30380C1756C565D5F9D76D583B \
  | sq keyring filter --experimental --cert F2B41200C54EFB30380C1756C565D5F9D76D583B --output update.pgp
sq keyring merge gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg update.pgp | sq packet dearmor --output gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg.new
mv gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg.new gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg
+++ refreshed/gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg
@@ -1,13 +1,13 @@
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
+self-signatures PositiveCertification: 2014-08-27, 2014-09-12, 2023-09-14, 2024-01-12
 self-signatures SubkeyBinding: 2014-08-27
+third-party GenericCertification: 5
+third-party PositiveCertification: 1
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the changed spec does not get past the signature check. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
