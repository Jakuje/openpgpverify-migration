# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show libuv`).

This switches the upstream source signature check from a direct GnuPG call (`gpgv2`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The spec called GnuPG itself instead of using `%gpgverify`; the check becomes one `%openpgpverify` call with the same keyring, signature and data.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- the direct `gpgv2` call is replaced by `%{openpgpverify}` with the same keyring, signature and data
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- refreshed keyring `keysuv.gpg` (see below); the comment above its `Source` line now shows the commands for refreshing it

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`gpgv2`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-26 at dist-git commit `a17f04ba152d` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `gpgv2` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `612F0EAD9401622379DF4402F28C3C8DA33C03BE`
- `C82FA3AE1CBEDC6BE46B9360C43CEC45C17AB93C`
- `CFBB9CA9A5BEAFD70E2B3C5A79A67C55A3679C8B`
- `AEAD0A4B686767751A0E4AEF34A25FB128246514`
- `57353E0DBDAAA7E839B66A1AFF47D5E4AD8B4FDC`
- `94AE36675C464D64BAFA68DD7434390BDBE9B9C5`
- `FDF519364458319FA8233DC9410E5553AE9BC059`
- `D77B1E34243FBAF05F8E9CC34F55C8C846AB89B9`

The refresh, as run (the spec comment above the `Source` line has the same commands, for the next refresh):

```
sq --home=none network search --output - 612F0EAD9401622379DF4402F28C3C8DA33C03BE C82FA3AE1CBEDC6BE46B9360C43CEC45C17AB93C CFBB9CA9A5BEAFD70E2B3C5A79A67C55A3679C8B AEAD0A4B686767751A0E4AEF34A25FB128246514 57353E0DBDAAA7E839B66A1AFF47D5E4AD8B4FDC 94AE36675C464D64BAFA68DD7434390BDBE9B9C5 FDF519364458319FA8233DC9410E5553AE9BC059 D77B1E34243FBAF05F8E9CC34F55C8C846AB89B9 \
  | sq keyring filter --experimental --cert 612F0EAD9401622379DF4402F28C3C8DA33C03BE --cert C82FA3AE1CBEDC6BE46B9360C43CEC45C17AB93C --cert CFBB9CA9A5BEAFD70E2B3C5A79A67C55A3679C8B --cert AEAD0A4B686767751A0E4AEF34A25FB128246514 --cert 57353E0DBDAAA7E839B66A1AFF47D5E4AD8B4FDC --cert 94AE36675C464D64BAFA68DD7434390BDBE9B9C5 --cert FDF519364458319FA8233DC9410E5553AE9BC059 --cert D77B1E34243FBAF05F8E9CC34F55C8C846AB89B9 --output update.pgp
sq keyring merge keysuv.gpg update.pgp | sq packet dearmor --output keysuv.gpg.new
mv keysuv.gpg.new keysuv.gpg
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/keysuv.gpg
+++ refreshed/keysuv.gpg
@@ -1,19 +1,17 @@
       Fingerprint: 612F0EAD9401622379DF4402F28C3C8DA33C03BE
-                   Invalid: The primary key is not live: Expired on 2025-06-28T22:21:50Z
-  Expiration time: 2025-06-28 22:21:50 UTC (creation time + 8years 10months 2days 4h 52m 2s)
+  Expiration time: 2030-06-29 16:54:38 UTC (creation time + 13years 10months 2days 17h 24m 50s)
         Key flags: certification, signing
            Subkey: 789091C99345138DF82158EF9221D4B6ABB7F18A
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-06-28T22:21:50Z
-  Expiration time: 2025-06-28 22:22:00 UTC (creation time + 8years 10months 2days 4h 52m 12s)
+  Expiration time: 2030-06-29 16:53:19 UTC (creation time + 13years 10months 2days 17h 23m 31s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Santiago Gimeno (sgimeno) <santiago.gimeno@gmail.com>
       Fingerprint: C82FA3AE1CBEDC6BE46B9360C43CEC45C17AB93C
-                   Invalid: No binding signature at time 2026-10-27T10:59:05Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: certification, signing
            Subkey: C4960C6DAA2AEBC352F3E5B8E140F61BC5979DCC
-                   Invalid: primary key: No binding signature at time 2026-10-27T10:59:05Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+        Key flags: transport encryption, data-at-rest encryption
+           UserID: Richard Lau <richard.lau@ibm.com>
            UserID: Richard Lau <riclau@uk.ibm.com>
                    Revoked:
-                   Invalid: No binding signature at time 2026-10-27T10:59:05Z
            UserID: Richard Lau <rlau@redhat.com>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
@@ -69,5 +67,10 @@
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
 self-signatures CertificationRevocation: 2021-06-22
-self-signatures PositiveCertification: 2012-07-24, 2013-06-12, 2015-07-21, 2018-10-26, 2020-09-25, 2020-10-01, 2021-07-07, 2022-03-05, 2023-06-29
-self-signatures SubkeyBinding: 2012-07-24, 2013-06-12, 2015-07-21, 2018-11-01, 2019-10-28, 2020-09-25, 2021-07-07, 2022-03-05, 2023-06-29
+self-signatures GenericCertification: 2022-03-05
+self-signatures PositiveCertification: 2012-07-24, 2013-06-12, 2015-07-21, 2016-08-26, 2018-10-26, 2019-10-28, 2020-02-07, 2020-09-25, 2020-10-01, 2021-07-07, 2022-03-05, 2023-06-29, 2025-06-25, 2025-06-30
+self-signatures SubkeyBinding: 2012-07-24, 2013-06-12, 2015-07-21, 2016-08-26, 2018-11-01, 2019-10-28, 2020-02-07, 2020-09-25, 2021-07-07, 2022-03-05, 2023-06-29, 2025-06-30
+third-party CasualCertification: 2
+third-party GenericCertification: 18
+third-party PersonaCertification: 1
+third-party PositiveCertification: 4
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the changed spec does not get past the signature check. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
