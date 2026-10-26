# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show keepassxc`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- refreshed keyring `keepassxc_master_signing_key.asc` (see below)
- Release bumped (`3%{?dist}` → `4%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-26 at dist-git commit `4c2b501cbd61` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `BF5A669F2272CF4324C1FDA8CFB4C2166397D0D2`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/keepassxc_master_signing_key.asc
+++ refreshed/keepassxc_master_signing_key.asc
@@ -1,22 +1,18 @@
       Fingerprint: BF5A669F2272CF4324C1FDA8CFB4C2166397D0D2
         Key flags: certification, signing
            Subkey: 71D4673D73C7F83C17DAE6A2D8538E98A26FD9C4
-                   Invalid: The subkey is not live: Expired on 2024-12-04T12:58:36Z
-  Expiration time: 2024-12-04 12:58:36 UTC (creation time + 7years 11months 4h 16m 27s)
+  Expiration time: 2028-12-08 21:43:56 UTC (creation time + 11years 11months 4days 13h 1m 47s)
         Key flags: signing
            Subkey: AF0AEA44ABAC8F1047733EA7AFF235EEFB5A2517
-                   Revoked:
-                   Invalid: The subkey is not live: Expired on 2021-01-07T18:49:30Z
-  Expiration time: 2021-01-07 18:49:30 UTC (creation time + 4years 4days 6m 18s)
+  Expiration time: 2028-12-08 21:43:56 UTC (creation time + 11years 11months 4days 12h 51m 8s)
         Key flags: signing
            Subkey: C1E4CBA3AD78D3AFD894F9E0B7A66F03B59076A8
-                   Invalid: The subkey is not live: Expired on 2024-12-04T12:59:25Z
-  Expiration time: 2024-12-04 12:59:25 UTC (creation time + 7years 11months 4h 5m 55s)
+  Expiration time: 2028-12-08 21:43:56 UTC (creation time + 11years 11months 4days 12h 50m 26s)
         Key flags: signing
            UserID: KeePassXC Release <release@keepassxc.org>
 self-signatures PositiveCertification: 2017-01-03, 2019-01-08
-self-signatures SubkeyBinding: 2019-01-08, 2020-12-05
+self-signatures SubkeyBinding: 2017-01-03, 2019-01-08, 2020-12-05, 2023-12-10
 self-signatures SubkeyRevocation: 2019-10-25
 third-party CasualCertification: 2
-third-party GenericCertification: 56
+third-party GenericCertification: 85
 third-party PositiveCertification: 2
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the changed spec does not get past the signature check. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
