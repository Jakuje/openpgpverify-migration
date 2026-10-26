# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show ntpsec`).

This switches the upstream source signature check from `%gpgverify` (GnuPG `gpgv`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The macro takes the same options, so the call itself only changes its name.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- refreshed keyring `ntpsec.gpg.pub.asc` (see below)
- Release bumped (`1%{?dist}` → `2%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-23 at dist-git commit `4d9ab763e0d2` with sequoia-sqv ? (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `DA3FDF774CC70FA64729EC4505D9B371477C7528`
- `E57235D22764129FA4F2F4D17F52608ED0E49D76`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/ntpsec.gpg.pub.asc
+++ refreshed/ntpsec.gpg.pub.asc
@@ -3,16 +3,15 @@
         Key flags: certification, signing
            Subkey: F1B3A359ACD57A7BFE493ABFAE3C53420F49D2EF
         Key flags: transport encryption, data-at-rest encryption
+           UserID: NTPsec Contact <contact@ntpsec.org>
            UserID: NTPsec Security Reporting <security@ntpsec.org>
       Fingerprint: E57235D22764129FA4F2F4D17F52608ED0E49D76
-                   Invalid: The primary key is not live: Expired on 2025-10-05T04:11:25Z
-  Expiration time: 2025-10-05 04:11:25 UTC (creation time + 4years 11months 29days 3h 50m 24s)
+  Expiration time: 2028-07-30 04:21:41 UTC (creation time + 7years 9months 23days 7h 7m 52s)
         Key flags: certification, signing
            Subkey: 4068094035426D1F8F8AA800F8FE4D92CC4090B5
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-10-05T04:11:25Z
-  Expiration time: 2025-10-05 04:11:25 UTC (creation time + 4years 11months 29days 3h 50m 24s)
+  Expiration time: 2028-07-30 04:23:52 UTC (creation time + 7years 9months 23days 7h 10m 3s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: NTPsec Security Reporting <security@ntpsec.org>
-self-signatures PositiveCertification: 2016-04-14, 2020-10-06
-self-signatures SubkeyBinding: 2020-10-06
-third-party GenericCertification: 1
+self-signatures PositiveCertification: 2016-04-14, 2017-02-22, 2020-10-06, 2026-07-31
+self-signatures SubkeyBinding: 2016-04-14, 2020-10-06, 2026-07-31
+third-party GenericCertification: 2
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the changed spec does not get past the signature check. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
