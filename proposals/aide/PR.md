# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show aide`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- refreshed keyring `gpgkey-aide.gpg` (see below); the comment above its `Source` line now shows the commands for refreshing it

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-12 at dist-git commit `37a89e90ec4c` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keys.openpgp.org, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `2BBBD30FAAB29B3253BCFBA6F6947DAB68E7B931`

The refresh, as run (the spec comment above the `Source` line has the same commands, for the next refresh):

```
sq --home=none network search --output - 2BBBD30FAAB29B3253BCFBA6F6947DAB68E7B931 \
  | sq keyring filter --experimental --cert 2BBBD30FAAB29B3253BCFBA6F6947DAB68E7B931 --output update.pgp
sq keyring merge gpgkey-aide.gpg update.pgp | sq packet dearmor --output gpgkey-aide.gpg.new
mv gpgkey-aide.gpg.new gpgkey-aide.gpg
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/gpgkey-aide.gpg
+++ refreshed/gpgkey-aide.gpg
@@ -1,20 +1,19 @@
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
+third-party CasualCertification: 2
+third-party GenericCertification: 20
+third-party PositiveCertification: 3
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: the spec has a `%check` section or uses gpg elsewhere, and tests may need it. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
