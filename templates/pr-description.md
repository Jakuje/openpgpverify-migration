This switches the upstream source signature check from `%gpgverify` (GnuPG) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The goal is that building packages no longer needs GnuPG to verify sources; RHEL 11 plans to ship without GnuPG. The new macro takes the same options, so the call itself only changes its name.

### Changes

$changes
### Testing

The current and the changed spec were both run through `$stage` in a clean mock chroot without network access ($chroots). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`%gpgverify`) | $calls_old | $result_old |
| this PR (`%openpgpverify`) | $calls_new | $result_new |

Tested on $tested_on at dist-git commit `$commit` with sequoia-sqv $sqv_version (Fedora DEFAULT crypto policy).
$refresh_section$notes_section
### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
