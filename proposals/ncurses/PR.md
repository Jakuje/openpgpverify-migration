# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show ncurses`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- dropped `BuildRequires: gcc gcc-c++ gnupg2 make pkgconfig`, only needed for `%gpgverify`
- refreshed keyring `dickey@invisible-island.net-rsa3072.asc` (see below); the comment above its `Source` line now shows the commands for refreshing it
- Release bumped (`3%{?dist}` → `4%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64, fedora-eln-x86_64, where even the current spec cannot install its build dependencies). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-12 at dist-git commit `b2310702e7f6` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `19882D92DDA4C400C22C0D56CC2AF4472167BE03`

The refresh, as run (the spec comment above the `Source` line has the same commands, for the next refresh):

```
sq --home=none network search --output - 19882D92DDA4C400C22C0D56CC2AF4472167BE03 \
  | sq keyring filter --experimental --cert 19882D92DDA4C400C22C0D56CC2AF4472167BE03 --output update.pgp
sq keyring merge --output dickey@invisible-island.net-rsa3072.asc.new dickey@invisible-island.net-rsa3072.asc update.pgp
mv dickey@invisible-island.net-rsa3072.asc.new dickey@invisible-island.net-rsa3072.asc
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/dickey@invisible-island.net-rsa3072.asc
+++ refreshed/dickey@invisible-island.net-rsa3072.asc
@@ -1,11 +1,12 @@
       Fingerprint: 19882D92DDA4C400C22C0D56CC2AF4472167BE03
-                   Invalid: The primary key is not live: Expired on 2023-07-30T23:08:24Z
-  Expiration time: 2023-07-30 23:08:24 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2029-04-02 01:56:22 UTC (creation time + 7years 8months 1day 20h 19m 10s)
         Key flags: certification, signing
            Subkey: 711EBE244DE66E56020CCB474C5C495AB79670BF
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2023-07-30T23:08:24Z
-  Expiration time: 2023-07-30 23:08:24 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2029-04-02 01:57:11 UTC (creation time + 7years 8months 1day 20h 19m 59s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Thomas E. Dickey (self-signed w/o SHA1) <dickey@invisible-island.net>
-self-signatures PositiveCertification: 2021-07-30
-self-signatures SubkeyBinding: 2021-07-30
+           UserID: Thomas E. Dickey (use for email) <dickey@his.com>
+self-signatures PositiveCertification: 2021-07-30, 2022-01-31, 2022-10-31, 2023-12-10, 2026-01-18
+self-signatures SubkeyBinding: 2021-07-30, 2022-10-31, 2023-12-10, 2026-01-18
+third-party CasualCertification: 1
+third-party GenericCertification: 2
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
