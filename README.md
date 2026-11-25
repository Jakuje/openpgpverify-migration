# %gpgverify → %openpgpverify migration

Fedora packages that check upstream source signatures do it with GnuPG,
through `%gpgverify` or by calling `gpg`/`gpgv` directly. This project moves
them to `%openpgpverify` (Sequoia `sqv`), which follows the system crypto
policy, checks that the key was valid when the release was signed, and
supports the current OpenPGP standard. ELN packages go first, so that
`%gpgverify` does not reach RHEL.

- Change: https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify (FESCo #3660, tracker rhbz#2523619)
- Package bugs: block [rhbz#2569052](https://bugzilla.redhat.com/show_bug.cgi?id=2569052)
- ELN coordination: [fedora-eln/eln#610](https://github.com/fedora-eln/eln/issues/610)

Every change is scripted and tested in mock before a PR goes out; how is
described in [docs/process.md](docs/process.md).

## Status (2026-11-25)

On 2026-10-06, 594 packages verified sources with GnuPG.

| | Packages | |
|---|---|---|
| Converted to `%openpgpverify` in rawhide | 327 | 55 % |
| PR open | 139 | 23 % |
| Retired, or signature check dropped | 6 | |
| Still to do | 122 | 21 % |

Of the 122 still to do, 107 are blocked on the upstream key (a bug is filed
for each: mostly DSA keys and SHA-1 self-signatures, a few expired keys), and 12 have a
tested PR that is not opened yet.

ELN: 106 of 164 converted, 28 PRs open, 25 blocked on the upstream key;
sssd's change was merged upstream and comes with the next rebase.

Latest reports: [progress](reports/progress-2026-11-25.md) (all packages,
with what changed since the previous report) and
[ELN](reports/eln-2026-11-25.md) (per package). Patches and PR texts are in
[proposals/](proposals/).

## Remaining work

- **Open PRs** (134): as of 2026-11-23, 125 had had no response for 2.5+ weeks and 2 are
  approved but not merged; Yaakov Selkowitz is merging them as a proven
  packager. They are listed for a proven packager in
  [announce/provenpackager-2026-11-23.md](announce/provenpackager-2026-11-23.md).
- **ELN builds**: a change merged in rawhide reaches ELN only with a new
  rawhide build; 39 ELN packages were last built before their change (2026-11-25).
- **Bugs** (107): follow up; when upstream publishes a fixed key, turn the bug
  into a PR (`scripts/refresh_keys.py propose-upstream`). Responses are
  recorded with `scripts/bug_response.py`.
- **Prepared, not opened** (11): python-oslo-config (waits for its PR #11),
  and 10 that fail to build in rawhide even without the change. The 8 keyring
  updates (Apache `KEYS` converted by GnuPG to drop the v3 keys sqv cannot
  read; the signer's key from keyservers for e2fsprogs, gnucobol, libextractor
  and tor) and fedrq went out as PRs on 2026-11-24.
- **cgit**: its own key is fixed, but it also verifies the bundled git
  tarball, signed with the same key as git (SHA-1 self-signatures); filed as
  [rhbz#2583259](https://bugzilla.redhat.com/show_bug.cgi?id=2583259), next to
  git's rhbz#2569328.
- **crun**: the Packit sync of 1.31 (2026-11-12) replaced the spec with
  upstream's and undid [PR #159](https://src.fedoraproject.org/rpms/crun/pull-request/159);
  rawhide is back on `%gpgverify`. The fix belongs in upstream's
  `rpm/crun.spec`, with a `%gpgverify` fallback for RHEL 10 and older:
  [containers/crun#2486](https://github.com/containers/crun/pull/2486)
  ([proposals/crun-upstream/](proposals/crun-upstream/) has the first draft).
- **Later**, as a separate campaign: the 211 packages that ship `.asc`/`.sig`
  files without verifying them, and leftover `BuildRequires: gnupg2`.

## Decisions

| Topic | Decision |
|---|---|
| Branches | **rawhide only**. Maintainers decide whether to merge down. |
| ELN | Rawhide changes **must work in ELN**; `openpgpverify` is available there. |
| EPEL | `openpgpverify` is in EPEL 9 and 10 (not 8), so specs shared with EPEL are converted fully; no `%if` for EPEL. |
| Release | Specs without `%autochangelog` get a **Release bump** and a changelog entry. |
| Delivery | **PRs first**. If maintainers don't respond, a provenpackager. |
| openpgpverify itself | **No changes**; in particular SHA-1 key bindings stay rejected (2026-10-08). Keyrings sqv cannot read are fixed in the PRs, keys only upstream can fix get a bug. |
| Keys expired before signing | **Stay rejected**. Sequoia upstream considers this a security feature: usually the keyring is just outdated, but hiding the failure could hide a leaked key. Fixed by a keyring refresh with the extended key, or a bug. |
| Keyring updates | Preferably the file upstream publishes, byte for byte; otherwise a keyserver copy of the same key. Every update is reviewed by hand, and is its own commit in the PR. |
| Announcement | The work is part of the approved Change, so the FESCo mass package change process was not used; a heads-up mail went to the devel list instead. This repository is public. |
| PR / commit texts | Technical and focused on Fedora's benefits. No emoji. AI disclosure only via the `Assisted-by:` commit trailer (Fedora AI contributions policy). |

## Documentation

- [docs/process.md](docs/process.md): the daily status update, the test
  harness, keyring refreshes, proposals and bugs, and the conversion rules
- [docs/gpgverify-vs-openpgpverify.md](docs/gpgverify-vs-openpgpverify.md):
  what passes with gpgverify but fails with openpgpverify, and why
- [docs/expired-keys-and-sha1.md](docs/expired-keys-and-sha1.md): expired keys
  and SHA-1, and what can and can't be fixed in openpgpverify
- [docs/data.md](docs/data.md): the starting inventory and the inventory and
  state record formats

## Layout

```
scripts/                 tooling
templates/               commit message, PR description and bug templates
manual/                  hand-written spec rewrites for direct gpg calls
proposals/               rendered patches, PR and bug texts
reports/                 progress, ELN and Phase 1 reports; keyring reviews
announce/                devel mail and ELN comment drafts, package lists
docs/                    process and background
reference/openpgpverify/ copy of the macro and wrapper script (from dist-git)
data/state/              per-package state (JSONL); the source of truth
data/inventory/          classifier output per snapshot
data/snapshots/          daily spec tarballs; not in git
work/                    dist-git clones and test logs; not in git
```
