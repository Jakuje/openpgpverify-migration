# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show bemenu`).

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
- refreshed keyring `bemenu-pgp.txt` (see below); the comment above its `Source` line now shows the commands for refreshing it

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-22 at dist-git commit `b8be10f8d655` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `16B6B7CACAF339DECE9F154729317348D687B86B`

The refresh, as run (the spec comment above the `Source` line has the same commands, for the next refresh):

```
sq --home=none network search --output - 16B6B7CACAF339DECE9F154729317348D687B86B \
  | sq keyring filter --experimental --cert 16B6B7CACAF339DECE9F154729317348D687B86B --output update.pgp
sq keyring merge --output bemenu-pgp.txt.new bemenu-pgp.txt update.pgp
mv bemenu-pgp.txt.new bemenu-pgp.txt
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/bemenu-pgp.txt
+++ refreshed/bemenu-pgp.txt
@@ -1,12 +1,8 @@
       Fingerprint: 16B6B7CACAF339DECE9F154729317348D687B86B
-                   Invalid: The primary key is not live: Expired on 2023-05-20T00:57:03Z
-  Expiration time: 2023-05-20 00:57:03 UTC (creation time + 1year 11months 29days 21h 50m 24s)
         Key flags: certification, signing
            Subkey: 553B84F554B6A81DCB701BB3662C8D5062CC4609
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2023-05-20T00:57:03Z
-  Expiration time: 2023-05-20 00:57:03 UTC (creation time + 1year 11months 29days 21h 50m 24s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Bemenu Upstream
-self-signatures PositiveCertification: 2021-05-20
-self-signatures SubkeyBinding: 2021-05-20
+self-signatures PositiveCertification: 2021-05-20, 2023-08-29
+self-signatures SubkeyBinding: 2021-05-20, 2023-08-29
 third-party GenericCertification: 1
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
