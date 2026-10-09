# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show yubikey-manager-qt`).

This switches the upstream source signature check from `%gpgverify` (GnuPG) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The goal is that building packages no longer needs GnuPG to verify sources; RHEL 11 plans to ship without GnuPG. The new macro takes the same options, so the call itself only changes its name.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- dropped `BuildRequires: gnupg2`, only needed for `%gpgverify`
- refreshed keyring `gpgkey-6690D8BC.gpg` (see below)

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-09 at dist-git commit `42f332dde60a` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `9E885C0302F9BB9167529C2D5CBA11E6ADC7BCD1`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/gpgkey-6690D8BC.gpg
+++ refreshed/gpgkey-6690D8BC.gpg
@@ -1,19 +1,16 @@
       Fingerprint: 9E885C0302F9BB9167529C2D5CBA11E6ADC7BCD1
-                   Invalid: The primary key is not live: Expired on 2020-09-16T11:49:44Z
-  Expiration time: 2020-09-16 11:49:44 UTC (creation time + 11months 30days 3h 50m 24s)
+  Expiration time: 2027-07-14 10:07:08 UTC (creation time + 7years 9months 26days 5h 15m)
         Key flags: certification
            Subkey: D6919FBF48C484F3CB7B71CD870B88256690D8BC
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2020-09-16T11:49:44Z
-  Expiration time: 2020-09-16 12:17:43 UTC (creation time + 11months 30days 3h 50m 24s)
+  Expiration time: 2027-07-14 10:08:26 UTC (creation time + 7years 9months 26days 4h 48m 19s)
         Key flags: signing
            Subkey: BBD85659722519CD52316CA699250E21D6F11774
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2020-09-16T11:49:44Z
-  Expiration time: 2020-09-16 11:55:25 UTC (creation time + 11months 30days 3h 50m 24s)
+  Expiration time: 2027-07-14 10:08:26 UTC (creation time + 7years 9months 26days 5h 10m 37s)
         Key flags: transport encryption, data-at-rest encryption
            Subkey: 95D3D9E90BA66C89CEA7838DF401E8A14F5D4E60
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2020-09-16T11:49:44Z
-  Expiration time: 2020-09-16 12:20:37 UTC (creation time + 11months 30days 3h 50m 24s)
+  Expiration time: 2027-07-14 10:08:26 UTC (creation time + 7years 9months 26days 4h 45m 25s)
         Key flags: authentication
            UserID: Dennis Fokin <dennis.fokin@yubico.com>
-self-signatures PositiveCertification: 2019-09-17
-self-signatures SubkeyBinding: 2019-09-17
+self-signatures PositiveCertification: 2019-09-17, 2020-09-14, 2021-09-07, 2022-09-07, 2023-08-02, 2025-07-14
+self-signatures SubkeyBinding: 2019-09-17, 2020-09-14, 2021-09-07, 2022-09-07, 2023-08-02, 2025-07-14
+third-party GenericCertification: 2
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is in Fedora 43 and later, but not in EPEL yet, so please keep `%gpgverify` on EPEL branches.
- No Release bump: nothing changes in the built packages, so no rebuild is needed now. The new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
