# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show inn`).

This switches the upstream source signature check from a direct GnuPG call (`gpgv2`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The spec called GnuPG itself instead of using `%gpgverify`; the check becomes one `%openpgpverify` call with the same keyring, signature and data.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- the direct `gpgv2` call is replaced by `%{openpgpverify}` with the same keyring, signature and data
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- dropped `BuildRequires: %{_bindir}/gpgv2`, only needed for the GnuPG verification
- refreshed keyring `0xD73934B49674CF5CCD9AC2787D80315C5736DE75.gpg` (see below); the comment above its `Source` line now shows the commands for refreshing it
- Release bumped (`5%{?dist}` → `6%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`gpgv2`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-26 at dist-git commit `2ed441cc9b59` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `gpgv2` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `E784364E8DDE7BB370FBD9EAD15D313882004173`

The refresh, as run (the spec comment above the `Source` line has the same commands, for the next refresh):

```
sq --home=none network search --output - E784364E8DDE7BB370FBD9EAD15D313882004173 \
  | sq keyring filter --experimental --cert E784364E8DDE7BB370FBD9EAD15D313882004173 --output update.pgp
sq keyring merge 0xD73934B49674CF5CCD9AC2787D80315C5736DE75.gpg update.pgp | sq packet dearmor --output 0xD73934B49674CF5CCD9AC2787D80315C5736DE75.gpg.new
mv 0xD73934B49674CF5CCD9AC2787D80315C5736DE75.gpg.new 0xD73934B49674CF5CCD9AC2787D80315C5736DE75.gpg
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/0xD73934B49674CF5CCD9AC2787D80315C5736DE75.gpg
+++ refreshed/0xD73934B49674CF5CCD9AC2787D80315C5736DE75.gpg
@@ -1,23 +1,25 @@
       Fingerprint: E784364E8DDE7BB370FBD9EAD15D313882004173
-                   Invalid: The primary key is not live: Expired on 2023-09-19T05:24:13Z
-  Expiration time: 2023-09-19 05:24:13 UTC (creation time + 14years 3months 21days 7h 21m 47s)
+  Expiration time: 2029-10-05 22:59:08 UTC (creation time + 20years 4months 8days 2h 23m 6s)
         Key flags: certification, signing
            Subkey: D73934B49674CF5CCD9AC2787D80315C5736DE75
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2023-09-19T05:24:13Z
-  Expiration time: 2021-09-19 05:25:18 UTC (creation time + 11years 1day 12h 3m 6s)
+  Expiration time: 2027-10-06 23:00:39 UTC (creation time + 17years 18days 17h 38m 27s)
         Key flags: signing
            Subkey: E374EC5D787B50348D17E57C7CE29A76E9769486
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2023-09-19T05:24:13Z
-  Expiration time: 2023-09-19 05:24:56 UTC (creation time + 14years 3months 21days 7h 4m 30s)
+  Expiration time: 2029-10-05 22:59:48 UTC (creation time + 20years 4months 8days 2h 5m 46s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Russ Allbery <eagle@eyrie.org>
            UserID: Russ Allbery <eagle@windlord.stanford.edu>
                    Revoked:
-                   Invalid: No binding signature at time 2026-10-27T10:55:23Z
            UserID: Russ Allbery <rra@cpan.org>
            UserID: Russ Allbery <rra@cs.stanford.edu>
            UserID: Russ Allbery <rra@debian.org>
+           UserID: Russ Allbery <rra@isc.org>
+           UserID: Russ Allbery <rra@lsst.org>
            UserID: Russ Allbery <rra@stanford.edu>
-self-signatures CertificationRevocation: 2014-08-16
-self-signatures PositiveCertification: 2018-09-18, 2020-09-19
-self-signatures SubkeyBinding: 2020-09-19
+                   Revoked:
+self-signatures CertificationRevocation: 2014-08-16, 2019-09-29
+self-signatures PositiveCertification: 2009-05-29, 2010-09-17, 2011-09-20, 2012-09-16, 2014-08-16, 2014-08-29, 2014-09-18, 2016-09-17, 2016-10-27, 2018-09-18, 2020-01-28, 2020-09-19, 2022-07-16, 2022-09-20, 2024-09-24, 2026-10-06
+self-signatures SubkeyBinding: 2009-05-29, 2010-09-17, 2011-03-18, 2011-09-20, 2012-03-17, 2012-09-16, 2013-03-16, 2013-09-16, 2014-03-16, 2014-09-18, 2015-03-21, 2015-09-18, 2016-03-17, 2016-09-17, 2017-03-18, 2017-09-16, 2018-03-17, 2018-09-18, 2019-03-16, 2019-09-29, 2020-03-29, 2020-09-19, 2021-03-20, 2021-09-19, 2022-03-20, 2022-09-20, 2023-03-25, 2023-10-20, 2024-03-17, 2024-09-24, 2025-03-17, 2025-10-08, 2026-04-17, 2026-10-06
+third-party CasualCertification: 6
+third-party GenericCertification: 48
+third-party PositiveCertification: 6
```

The keyring change is the first of the two commits, so it can be reviewed or merged on its own.

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
