# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show time`).

This switches the upstream source signature check from `%gpgverify` (GnuPG) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The goal is that building packages no longer needs GnuPG to verify sources; RHEL 11 plans to ship without GnuPG. The new macro takes the same options, so the call itself only changes its name.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- refreshed keyring `gpgkey-F576AAAC1B0FF849792D8CB129A794FD2272BC86.gpg` (see below)
- changelog entry (1.9-29), without a Release bump

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-09 at dist-git commit `c59b262763d1` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` rejected the signature with the keyring in dist-git (keyring lacks older self-signatures), while `%gpgverify` ignores that. The same certificate, looked up by fingerprint (hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `F576AAAC1B0FF849792D8CB129A794FD2272BC86`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/gpgkey-F576AAAC1B0FF849792D8CB129A794FD2272BC86.gpg
+++ refreshed/gpgkey-F576AAAC1B0FF849792D8CB129A794FD2272BC86.gpg
@@ -12,8 +12,8 @@
         Key flags: transport encryption, data-at-rest encryption
            UserID: Assaf Gordon <agordon@wi.mit.edu>
                    Revoked:
-                   Invalid: No binding signature at time 2026-10-09T13:01:20Z
            UserID: Assaf Gordon <assafgordon@gmail.com>
 self-signatures CertificationRevocation: 2015-08-13
-self-signatures PositiveCertification: 2020-02-24
-self-signatures SubkeyBinding: 2020-02-24
+self-signatures PositiveCertification: 2014-07-09, 2015-08-12, 2017-01-19, 2018-02-14, 2020-02-24
+self-signatures SubkeyBinding: 2014-07-09, 2015-08-12, 2017-01-19, 2018-02-14, 2020-02-24
+third-party GenericCertification: 1
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is in Fedora 43 and later, but not in EPEL yet, so please keep `%gpgverify` on EPEL branches.
- `BuildRequires: gnupg2` is kept: the spec has a `%check` section or uses gpg elsewhere, and tests may need it. If it was only there for the signature check, it can go too.
- No Release bump: nothing changes in the built packages, so no rebuild is needed now. The new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
