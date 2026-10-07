# %gpgverify → %openpgpverify migration

Tooling and data for converting Fedora packages from GnuPG-based source
signature verification (`%gpgverify`, raw `gpg`/`gpgv2`) to Sequoia-based
`%openpgpverify`.

- Change: https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify
- FESCo ticket: #3660, tracker bug: rhbz#2523619

## Decisions

| Topic | Decision |
|---|---|
| Branches | **rawhide only**. Maintainers decide whether to merge down. |
| Delivery | **PRs first**. If maintainers don't respond, find a provenpackager. |
| Wrapper fixes (concatenated armor, keybox keyrings) | Decide **after Phase 1** results. |
| Unverified `.asc`/`.sig` sources (216), leftover `BR: gnupg2` (38) | **Later**, as a follow-up hardening campaign. |
| AI disclosure | `Assisted-by:` commit trailer (Fedora AI contributions policy). |

## Phases

0. **Inventory**: scan the daily all-specs tarball
   (`https://src.fedoraproject.org/lookaside/rpm-specs-latest.tar.xz`) and
   cross-check it against rawhide source repo BuildRequires.
1. **Side-by-side test (no builds)**: dist-git clone at rawhide HEAD, then
   `fedpkg sources`, `rpmspec -P` with no network (specs are untrusted code),
   then run each expanded gpgverify call with both gpgverify and openpgpverify.
   Outcomes: `both-pass`, `regression` (diagnose: keybox keyring, concatenated
   armor, SHA-1/DSA cert, expiry), or `both-fail` (pre-existing breakage).
2. **Rewrite the spec**: rename the macro, `BR: gpgverify` → `BR: openpgpverify`,
   drop `BR: gnupg2` only if gpg isn't used elsewhere, add a changelog entry
   unless the spec uses `%autochangelog`. Re-run the Phase 1 check and
   `rpmbuild -bp`.
3. **Rollout**: pilot (~15 own packages), announce on devel list/Discourse,
   then PR batches of 30–50 per day. Bugs blocking rhbz#2523619 for
   regressions caused upstream. Keep the forge layer swappable (Pagure →
   Forgejo migration).

## Layout

```
scripts/                 tooling
reference/openpgpverify/ copy of the macro and wrapper script (from dist-git)
data/snapshots/<date>/   raw inputs (spec tarball + extracted specs, repoquery dumps); not in git
data/snapshots/latest    symlink to the newest snapshot
data/inventory/          derived per-package classification
data/state/              per-package state records (JSONL), one source of truth for all phases
reports/                 generated summaries
```

## Inventory as of 2026-10-06

| Bucket | Packages |
|---|---|
| `%gpgverify`, one plain long-option call | 483 |
| `%gpgverify`, short options / reordered / multiple calls (macro supports all of these) | 77 |
| raw `gpg`/`gpgv2` in spec (manual work) | 45 |
| … of these inside `%if` blocks | 91 |
| already on `openpgpverify` | 7 |
| *(later)* signature sources never verified | 216 |
| *(later)* `BR: gnupg2` without source verification | 38 |

Inputs for the ~604 in-scope packages total about 4.9 GB (largest:
libreoffice, dotnet10.0, rust, llvm).

Reproduce the classification:

```
python3 -I scripts/classify.py data/snapshots/latest/rpm-specs data/inventory/classes-$(date -I).json
```

## State record (planned format)

```json
{"package": "libfoo", "commit": "abc123", "category": "macro-simple",
 "conditional": false, "calls": 1,
 "verify_old": "pass", "verify_new": "fail",
 "failure_reason": "sha1-cert", "diag": "stderr excerpt",
 "status": "needs-bug",
 "pr_url": null, "bug_id": null, "updated": "2026-10-06T18:00Z"}
```

Status flow: `inventory → tested → patched → prepped → pr-open → merged`,
or one of `needs-bug → bug-filed`, `manual`, `skipped`.

## TODO

- [ ] Install helpers: `fedpkg mock rpm-build rpmdevtools sequoia-sqv sequoia-sq openpgpverify gpgverify python3-bugzilla`
- [ ] Pagure (dist-git) API token, Bugzilla API key
- [ ] Phase 0: emit `data/state/packages.jsonl` from the classifier
- [ ] Phase 1 harness
