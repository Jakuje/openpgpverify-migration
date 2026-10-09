# Verify source signatures with openpgpverify

This switches the upstream source signature check from `%gpgverify` (GnuPG) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The goal is that building packages no longer needs GnuPG to verify sources; RHEL 11 plans to ship without GnuPG. The new macro takes the same options, so the call itself only changes its name.

### Changes

- `%gpgverify` → `%openpgpverify` (1 call; the macro keeps the same form and options)
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | pass |

Tested on 2026-10-09 at dist-git commit `bbba5cf6336b` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is in Fedora 43 and later, but not in EPEL yet, so please keep `%gpgverify` on EPEL branches.
- `BuildRequires: gnupg2` is kept: the spec has a `%check` section or uses gpg elsewhere, and tests may need it. If it was only there for the signature check, it can go too.
- No Release bump: nothing changes in the built packages, so no rebuild is needed now. The new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
