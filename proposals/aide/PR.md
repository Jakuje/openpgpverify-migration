# Verify source signatures with openpgpverify

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (2 calls; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- dropped `BuildRequires:  gnupg2`, only needed for `%gpgverify`
- replaced keyring `gpgkey-aide.gpg` with `gpgkey-aide.asc` from https://keys.openpgp.org/vks/v1/by-fingerprint/2BBBD30FAAB29B3253BCFBA6F6947DAB68E7B931#/gpgkey-aide.asc; its `Source` line is now that URL (see below)
- refreshed keyring `nettle-release-keyring.gpg` too (see below); it was in the lookaside cache, which a PR cannot update, so it moves into git (its line in `sources` is dropped)

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64, fedora-eln-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 2 | pass |
| this PR (`%openpgpverify`) | 2 | pass |

Tested on 2026-11-12 at dist-git commit `0f4a84ebbe7c` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (verification fails), while `%gpgverify` ignores that. The key owner has updated the key since: the copy at https://keys.openpgp.org/vks/v1/by-fingerprint/2BBBD30FAAB29B3253BCFBA6F6947DAB68E7B931#/gpgkey-aide.asc has the same fingerprint(s) and verifies the release with sqv. This PR replaces the file with that copy, byte for byte, named like the URL, which becomes its `Source`:

```
curl -fsSL -o gpgkey-aide.asc 'https://keys.openpgp.org/vks/v1/by-fingerprint/2BBBD30FAAB29B3253BCFBA6F6947DAB68E7B931'
```

Fingerprints (unchanged):

- `2BBBD30FAAB29B3253BCFBA6F6947DAB68E7B931`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/gpgkey-aide.gpg
+++ upstream/gpgkey-aide.gpg
@@ -1,20 +1,16 @@
       Fingerprint: 2BBBD30FAAB29B3253BCFBA6F6947DAB68E7B931
-                   Invalid: The primary key is not live: Expired on 2026-06-27T05:58:55Z
-  Expiration time: 2026-06-27 05:58:55 UTC (creation time + 14years 11months 29days 5h 43m 31s)
+  Expiration time: 2028-06-27 07:14:25 UTC (creation time + 16years 11months 29days 18h 59m 1s)
         Key flags: certification
            Subkey: 5495CDA17C9AC17AB23841A718EE86386022EF57
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-06-27T05:58:55Z
-  Expiration time: 2025-06-27 06:00:19 UTC (creation time + 13years 11months 29days 11h 42m 25s)
+  Expiration time: 2027-06-27 07:15:04 UTC (creation time + 15years 11months 29days 57m 10s)
         Key flags: signing
            Subkey: A6CCE790DD1E6669B7CD501057C198E495A601C7
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-06-27T05:58:55Z
-  Expiration time: 2025-06-27 06:00:51 UTC (creation time + 13years 11months 29days 11h 39m 43s)
+  Expiration time: 2027-06-27 07:15:19 UTC (creation time + 15years 11months 29days 54m 11s)
         Key flags: transport encryption, data-at-rest encryption
            Subkey: E22E962797F39BD6927E4AEDF4B483CB268B1790
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-06-27T05:58:55Z
-  Expiration time: 2025-06-27 06:00:51 UTC (creation time + 13years 11months 29days 11h 37m 42s)
+  Expiration time: 2027-06-27 07:15:32 UTC (creation time + 15years 11months 29days 52m 23s)
         Key flags: authentication
            UserID: Hannes von Haugwitz <hannes@vonhaugwitz.com>
            UserID: Hannes von Haugwitz <hvhaugwitz@debian.org>
-self-signatures PositiveCertification: 2023-06-04
-self-signatures SubkeyBinding: 2023-06-04
+self-signatures PositiveCertification: 2011-06-28, 2013-10-27, 2015-06-25, 2019-01-12, 2021-02-14, 2023-06-04, 2025-04-28, 2026-06-07
+self-signatures SubkeyBinding: 2011-06-28, 2013-05-09, 2015-06-25, 2017-07-01, 2019-01-12, 2021-02-14, 2023-06-04, 2025-04-28, 2026-06-07
```

### Bundled nettle keyring

The bundled nettle (built on RHEL/ELN, `%bcond bundled_nettle 0%{?rhel}`) is verified with `nettle-release-keyring.gpg`, the same file as in the nettle package. Its key had expired on 2025-01-15, so `%openpgpverify` rejected the nettle 4.0 signature in ELN. The file is replaced with the keyserver copy of the same key, byte for byte the keyring of [nettle#17](https://src.fedoraproject.org/rpms/nettle/pull-request/17), which extends the expiry to 2030. Exactly this command (also in the comment above its `Source` line):

```
sq --home=none network keyserver search 343C2FF0FBEE5EC2EDBEF399F3599FF828C67298 --output nettle-release-keyring.gpg --overwrite
```

Fingerprint (unchanged):

- `343C2FF0FBEE5EC2EDBEF399F3599FF828C67298`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/nettle-release-keyring.gpg
+++ refreshed/nettle-release-keyring.gpg
@@ -1,16 +1,14 @@
       Fingerprint: 343C2FF0FBEE5EC2EDBEF399F3599FF828C67298
-                   Invalid: The primary key is not live: Expired on 2025-01-15T17:12:43Z
-  Expiration time: 2025-01-15 17:12:43 UTC (creation time + 12years 7days 21h 46m 16s)
+  Expiration time: 2030-06-25 18:39:13 UTC (creation time + 17years 5months 16days 12h 24m 46s)
         Key flags: certification, signing
            Subkey: 48C9DE74746361F8617018347520153007F35B23
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-01-15T17:12:43Z
-  Expiration time: 2025-01-15 17:21:19 UTC (creation time + 12years 7days 21h 54m 52s)
+  Expiration time: 2030-06-25 18:40:52 UTC (creation time + 17years 5months 16days 12h 26m 25s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Niels Möller <nisse@lysator.liu.se>
-self-signatures PositiveCertification: 2013-01-07, 2020-01-17
-self-signatures SubkeyBinding: 2013-01-07, 2020-01-17
+self-signatures PositiveCertification: 2013-01-07, 2020-01-17, 2025-06-26
+self-signatures SubkeyBinding: 2013-01-07, 2020-01-17, 2025-06-26
 third-party CasualCertification: 7
 third-party CertificationRevocation: 1
-third-party GenericCertification: 16
+third-party GenericCertification: 18
 third-party PersonaCertification: 1
 third-party PositiveCertification: 3
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is dropped too. To check that nothing else needs it, the changed spec was built completely (`rpmbuild -bb`, including `%check`) in a chroot with gnupg2 and gpgverify removed, and neither the build log nor the test files in the sources mention gpg.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
