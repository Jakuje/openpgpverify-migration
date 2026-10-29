# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show webkitgtk`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- refreshed keyring `webkitgtk-keys.gpg` (see below); the comment above its `Source` line now shows the commands for refreshing it

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-26 at dist-git commit `a904230554c0` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `013A0127AC9C65B34FFA62526C1009B693975393`
- `5AA3BC334FD7E3369E7C77B291C559DBE4C9123B`

The refresh, as run (the spec comment above the `Source` line has the same commands, for the next refresh):

```
sq --home=none network search --output - 013A0127AC9C65B34FFA62526C1009B693975393 5AA3BC334FD7E3369E7C77B291C559DBE4C9123B \
  | sq keyring filter --experimental --cert 013A0127AC9C65B34FFA62526C1009B693975393 --cert 5AA3BC334FD7E3369E7C77B291C559DBE4C9123B --output update.pgp
sq keyring merge webkitgtk-keys.gpg update.pgp | sq packet dearmor --output webkitgtk-keys.gpg.new
mv webkitgtk-keys.gpg.new webkitgtk-keys.gpg
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/webkitgtk-keys.gpg
+++ refreshed/webkitgtk-keys.gpg
@@ -1,19 +1,17 @@
       Fingerprint: 013A0127AC9C65B34FFA62526C1009B693975393
-                   Invalid: The primary key is not live: Expired on 2026-04-09T10:58:53Z
-  Expiration time: 2026-04-09 10:58:53 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2028-04-19 07:53:36 UTC (creation time + 4years 9days 20h 54m 43s)
         Key flags: certification, signing
            Subkey: 5FB4EC8D6401C26F72B7B559B92AE30C7A82B686
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-04-09T10:58:53Z
-  Expiration time: 2026-04-09 10:58:53 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2028-04-19 07:57:41 UTC (creation time + 4years 9days 20h 58m 48s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Carlos Garcia Campos <cgarcia@igalia.com>
       Fingerprint: 5AA3BC334FD7E3369E7C77B291C559DBE4C9123B
                    Invalid: Policy rejected asymmetric algorithm: DSA1024 is not considered secure
            Subkey: 86578FD638E90525130ADF4976D146E5CE5D1038
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
                    Invalid: primary key: Policy rejected asymmetric algorithm, because DSA1024 is not considered secure
            UserID: Adrián Pérez de Castro (personal) <adrian@perezdecastro.org>
            UserID: Adrián Pérez de Castro <aperez@igalia.com>
-self-signatures PositiveCertification: 2024-04-09, 2024-04-14
-self-signatures SubkeyBinding: 2008-06-02, 2024-04-09
+self-signatures PositiveCertification: 2008-06-02, 2015-07-16, 2016-05-11, 2018-05-12, 2020-05-12, 2022-05-11, 2024-04-09, 2024-04-14, 2026-03-16, 2026-04-20
+self-signatures SubkeyBinding: 2008-06-02, 2024-04-09, 2026-03-16, 2026-04-20
+third-party CasualCertification: 1
+third-party GenericCertification: 13
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: sources over 40 MB, too large for the full build without gnupg2 on the test machine. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
