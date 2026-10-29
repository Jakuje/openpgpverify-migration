# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show b43-fwcutter`).

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
- refreshed keyring `757FAB7CED1814AE15B4836E5FB027474203454C.gpg` (see below); the comment above its `Source` line now shows the commands for refreshing it

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-22 at dist-git commit `17e03463680a` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `0392335A78083894A4301C43236E8A58C6DB4512`
- `69100FFB90E87A320DF8643CBEC39009E8321A61`
- `757FAB7CED1814AE15B4836E5FB027474203454C`

The refresh, as run (the spec comment above the `Source` line has the same commands, for the next refresh):

```
sq --home=none network search --output - 0392335A78083894A4301C43236E8A58C6DB4512 69100FFB90E87A320DF8643CBEC39009E8321A61 757FAB7CED1814AE15B4836E5FB027474203454C \
  | sq keyring filter --experimental --cert 0392335A78083894A4301C43236E8A58C6DB4512 --cert 69100FFB90E87A320DF8643CBEC39009E8321A61 --cert 757FAB7CED1814AE15B4836E5FB027474203454C --output update.pgp
sq keyring merge --output 757FAB7CED1814AE15B4836E5FB027474203454C.gpg.new 757FAB7CED1814AE15B4836E5FB027474203454C.gpg update.pgp
mv 757FAB7CED1814AE15B4836E5FB027474203454C.gpg.new 757FAB7CED1814AE15B4836E5FB027474203454C.gpg
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/757FAB7CED1814AE15B4836E5FB027474203454C.gpg
+++ refreshed/757FAB7CED1814AE15B4836E5FB027474203454C.gpg
@@ -25,14 +25,13 @@
         Key flags: transport encryption, data-at-rest encryption
            UserID: Ivan Alonso [Kaian] <kaian@irontec.com>
       Fingerprint: 757FAB7CED1814AE15B4836E5FB027474203454C
-                   Invalid: The primary key is not live: Expired on 2026-06-14T18:23:49Z
-  Expiration time: 2026-06-14 18:23:49 UTC (creation time + 14years 3months 24days 8h 21m 9s)
+  Expiration time: 2027-06-14 18:46:36 UTC (creation time + 15years 3months 24days 2h 43m 56s)
         Key flags: certification, signing
            Subkey: BC87DDC8C8254346D5F62B400988558F3A32F21D
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-06-14T18:23:49Z
-  Expiration time: 2026-06-14 18:24:26 UTC (creation time + 14years 3months 24days 8h 21m 46s)
+  Expiration time: 2027-06-14 18:46:47 UTC (creation time + 15years 3months 24days 2h 44m 7s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Michael Büsch (Git tag signing key) <m@bues.ch>
            UserID: Michael Büsch (Release signing key) <m@bues.ch>
-self-signatures PositiveCertification: 2012-02-19, 2013-03-01, 2013-08-10, 2014-03-02, 2015-03-04, 2016-03-03, 2018-01-09, 2018-03-03, 2019-03-02, 2020-02-22, 2020-05-21, 2021-03-31, 2023-04-15, 2024-04-16, 2025-06-14, 2025-10-16
-self-signatures SubkeyBinding: 2013-08-10, 2020-05-21, 2025-06-14
+self-signatures PositiveCertification: 2012-02-19, 2013-03-01, 2013-08-10, 2014-03-02, 2015-03-04, 2016-03-03, 2018-01-09, 2018-03-03, 2019-03-02, 2020-02-22, 2020-05-21, 2021-03-31, 2023-04-15, 2024-04-16, 2025-06-14, 2025-10-16, 2026-06-14
+self-signatures SubkeyBinding: 2012-02-19, 2013-03-01, 2013-08-10, 2014-03-02, 2015-03-04, 2016-03-03, 2018-01-09, 2018-03-03, 2019-03-02, 2020-02-22, 2020-05-21, 2021-03-31, 2023-04-15, 2024-04-16, 2025-06-14, 2026-06-14
+third-party GenericCertification: 1
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
