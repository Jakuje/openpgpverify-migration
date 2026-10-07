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
| ELN / RHEL | Rawhide changes **must work in ELN**. The goal is RHEL 11 without GnuPG. `openpgpverify` is available in ELN. No RHEL 10 / EPEL 10 backports for now (they may come later for compatibility). |
| Delivery | **PRs first**. If maintainers don't respond, find a provenpackager. |
| Wrapper fixes (concatenated armor, keybox keyrings) | Decide **after Phase 1** results. |
| Unverified `.asc`/`.sig` sources, leftover `BR: gnupg2` | **Later**, as a follow-up hardening campaign. |
| Policy | FESCo *Mass package changes* policy: announce on devel-announce and Discourse ≥ 1 week ahead, publish this repository. |
| AI disclosure | `Assisted-by:` commit trailer (Fedora AI contributions policy). |

## Known differences between gpgverify and openpgpverify

The command-line interface is the same (long options, `-k/-s/-d` short
options, `--keyrings`, `--data=-` from stdin). Same behaviour for armored,
binary and concatenated-armor keyrings, and expiry is checked at signature
time in both. Differences:

| Case | gpgverify | openpgpverify |
|---|---|---|
| GnuPG keybox (`.kbx`, usually named `*.gpg`) keyring | pass | **fail** |
| SHA-1 signature/certificate (DEFAULT crypto policy) | pass | **fail** |
| Several armored blocks in one signature file | pass | **fail** |
| Exit code for "no matching key" | 2 | 1 |
| stdout | quiet | prints fingerprint |
| `--output` | inline or cleartext | cleartext only, refuses to overwrite (only git-lfs uses it) |

The result depends on the Sequoia crypto policy, so the harness runs with the
system DEFAULT policy and records it (no `SEQUOIA_CRYPTO_POLICY` override).

## Conversion rules (Phase 2)

1. **Macro call**: keep the existing form exactly.
   - `%{gpgverify}` → `%{openpgpverify}`
   - `%gpgverify -k2 -s1 -d0` → `%openpgpverify -k2 -s1 -d0`
   - `%{?gpgverify:…}` → `%{?openpgpverify:…}`

   Never drop the braces: `%gpgverify --keyring=…` fails with *Unknown
   option -*.
2. **Always add `BuildRequires: openpgpverify`.** Only 75 in-scope specs have
   `BR: gpgverify`. Most get gpgverify implicitly through
   `redhat-rpm-config`'s `Requires: (gpgverify if gnupg2)`, others via
   `%{_bindir}/gpgv2`, `BR: %{gpgverify}`, or another package's dependency.
   Nothing pulls in openpgpverify that way.
3. **`BR: gpgverify`, `%{_bindir}/gpgv2`, `%{gpgverify}`**: drop them.
   **`BR: gnupg2`**: drop it only when `gnupg2_action == "remove"`, meaning
   the spec has no other gpg use and no `%check`. With `review` (has
   `%check`; tests often skip gpg silently when it's missing) or `keep`
   (other gpg use), leave it for the later hardening campaign.
4. **Release / changelog**: never bump `Release`. Specs with `%autochangelog`
   get nothing extra, and the commit subject becomes the changelog line. The
   others get a changelog entry with no Release bump.
5. **Raw gpg/gpgv calls** (`raw-verify`) are rewritten by hand into a macro
   call, piped through `--data=-` where the data is decompressed on the fly.
6. **RHEL conditionals**: rawhide and ELN both get openpgpverify, so the
   plain conversion is the default. Only where the verification or its BR is
   already in an `%if 0%{?rhel} …` block (spec shared with EPEL / CentOS /
   RDO) keep the old branch for older RHEL:

   ```
   %if 0%{?fedora} || 0%{?rhel} >= 11
   BuildRequires:  openpgpverify
   %else
   BuildRequires:  gnupg2
   %endif
   ...
   %if 0%{?fedora} || 0%{?rhel} >= 11
   %{openpgpverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
   %else
   %{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
   %endif
   ```

## Phases

0. **Inventory** (`scripts/classify.py`): scan the daily all-specs tarball
   (`https://src.fedoraproject.org/lookaside/rpm-specs-latest.tar.xz`) as
   text, cross-checked against the rawhide source repo.
1. **Side-by-side test**: for each in-scope package, at rawhide HEAD:
   1. dist-git clone and `fedpkg sources`.
   2. Run **`rpmbuild -bp --nodeps`** twice in a network-less rawhide/ELN
      container or mock root: once unchanged and once with the Phase 2
      rewrite. Define `fedora 45` / `dist .fc45`; run ELN (`rhel 11`) for
      `rhel_conditional` packages. Running the whole `%prep` (rather than
      extracted commands) covers the cases where the verify call depends on
      earlier `%prep` steps: stdin pipes, verification after `%setup`,
      per-arch Lua source selection, and `%{_sourcedir}` paths. Specs are
      untrusted code (`%(…)`, `%{lua:}`), so the sandbox is required.
   3. **Guard against verification that silently disappears**: the expanded
      spec (`rpmspec -P`, in a buildroot that has only the spec's BRs, not
      this host) must contain as many verify calls as the inventory found,
      and at least one. `%{?openpgpverify:…}` with a missing BR, or a call in
      a branch that evaluates false, would otherwise pass without verifying.
   4. Outcomes:
      - `both-pass`
      - `regression`: diagnose with `file` on each keyring (keybox), count the
        armor blocks, and `sq inspect` / `sq packet dump` for SHA-1, DSA and
        expiry
      - `both-fail`: the package was already broken; reported separately
2. **Rewrite the spec**: apply the conversion rules, then re-run Phase 1 on
   the result.
3. **Rollout**:
   1. Pilot with about 15 of our own packages.
   2. Announce.
   3. Open PRs in batches of 30–50 per day. Before each PR, check for open
      PRs touching the spec and skip retired or orphaned packages.
   4. File bugs blocking rhbz#2523619 for regressions that need upstream
      action.
   5. After a fixed period without a response, ask a provenpackager and
      point to the approved Change.

   Keep the forge layer swappable (dist-git is moving from Pagure to
   Forgejo).

## Layout

```
scripts/                 tooling
reference/openpgpverify/ copy of the macro and wrapper script (from dist-git)
data/snapshots/<date>/   raw inputs (spec tarball + extracted specs, repoquery dumps); not in git
data/snapshots/latest    symlink to the newest snapshot
data/inventory/          classifier output per snapshot (regenerable)
data/state/              per-package state records (JSONL); the single mutable source of truth for Phases 1–3
reports/                 generated summaries
```

## Inventory as of 2026-10-06

```
python3 -I scripts/classify.py data/snapshots/latest/rpm-specs \
    data/inventory/inventory-2026-10-06.jsonl data/snapshots/latest/rawhide-srpm-sizes.txt
```

| Category | Packages | Notes |
|---|---|---|
| `macro-simple` | 425 | `%prep` call(s) with `%{SOURCEn}` args only, no `%if`, no pipe, before `%setup` |
| `macro-complex` | 133 | everything else using the macro (see below) |
| `raw-verify` | 36 | direct `gpgv2`/`gpg --verify` (openssh, qemu, libreoffice, samba family, …); converted by hand |
| **in scope** | **594** | about 4.9 GB of sources; libredwg is not in the rawhide repo |
| `converted` | 5 | kryoptic, libfido2, libgcrypt, pam-u2f, wdiff |
| `sequoia-native` | 2 | archlinux-keyring, dnsmasq (call `sq`/`sqv` directly) |
| `dscverify` | 1 | whois; out of scope |
| *(later)* `sig-unverified` | 211 | ships `.asc`/`.sig`, never verifies (1.3 GB) |
| *(later)* `gnupg2-br-only` | 46 | gpg BR but no source verification (tests, leftovers) |

Details for the 594 in-scope packages:

| Property | Count |
|---|---|
| verify inside `%if` | 88 |
| `%{?rhel}`/EPEL conditional around the verify call or its BR | 10 (asterisk, bind9-next, dhcpcd, fapolicyd, git, openresolv, rust, samba, sssd, unbound) |
| spec mentions `%{?rhel}` anywhere | 122 |
| optional `%{?gpgverify:…}` (can disappear silently) | 5 (getdns, php, phpMyAdmin, rnp, roundcubemail) |
| several calls | 17 |
| data piped via stdin | 15 |
| verify after `%setup` | 18 |
| verify outside `%prep` | 3 (libstrophe, libtalloc, libtdb) |
| `BR: gpgverify` / `BR: gnupg2` / path or macro BR / no gpg BR at all | 75 / 467 / 37 / 19 |
| `gnupg2_action` remove / review / keep | 165 / 272 / 30 |
| `%autochangelog` / manual changelog | 286 / 308 |

## Inventory record (`data/inventory/*.jsonl`)

One line per relevant package, produced from the spec text only:

```json
{"package": "libfoo", "category": "macro-simple", "in_scope": true,
 "calls": [{"line": 42, "section": "prep", "form": "braced",
            "args": "--keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'",
            "stdin": false, "after_setup": false, "conditions": [], "simple": true}],
 "forms": ["braced"], "raw_verify": [], "gpg_other": [], "openpgpverify_calls": 0,
 "sequoia_native": false, "dscverify": false, "sig_sources": ["Source1"],
 "br": {"gpgverify": false, "gnupg2": true, "gpgv2_path": false, "macro": false, "openpgpverify": false},
 "gnupg2_action": "review", "has_check": true,
 "conditional": false, "rhel_conditional": false, "mentions_rhel": false,
 "autochangelog": true, "autorelease": true, "in_rawhide": true, "srpm_size": 1234567}
```

`form` is one of `braced`, `short`, `optional`, or `unbraced-long` (broken).

## State record (`data/state/packages.jsonl`, planned)

Created from the inventory and updated by every later step. Each step reads
and writes it, so steps can be resumed and re-run safely:

```json
{"package": "libfoo", "category": "macro-simple",
 "spec_commit": "abc123", "spec_sha256": "…",
 "maintainers": ["…"], "existing_prs": [], "eln_relevant": false,
 "harness_version": "1", "sqv_version": "…", "crypto_policy": "DEFAULT",
 "results": [{"call": 0, "expanded": "…", "old_rc": 0, "new_rc": 1,
              "keyring_format": "keybox", "failure_reason": "keybox",
              "diag": "stderr excerpt"}],
 "expanded_calls_old": 1, "expanded_calls_new": 1,
 "status": "regression",
 "pr_url": null, "bug_id": null,
 "announced": null, "nag_sent": null, "escalated": null,
 "updated": "2026-10-06T18:00Z"}
```

Statuses:

- Main path: `inventory → tested → patched → prepped → pr-open → merged → built`
- Phase 1 outcomes: `both-fail`, `regression → bug-filed`
- After a PR is opened: `pr-rejected`, `superseded` (the maintainer did it),
  `needs-rebase` (spec changed since `spec_sha256`)
- Other: `manual`, `skipped`

Verification only actually runs when the package is built, so `merged` and
`built` are tracked separately.

## TODO

- [x] Install helpers (fedpkg, mock, rpm-build, rpmdevtools, sequoia-sqv, sequoia-sq, openpgpverify, gpgverify, python3-bugzilla)
- [x] Phase 0 inventory (`scripts/classify.py`)
- [ ] Pagure (dist-git) API token, Bugzilla API key
- [ ] Seed `data/state/packages.jsonl` from the inventory (+ maintainers from `pagure_owner_alias.json`)
- [ ] Phase 1 harness: pilot on a sample covering every pattern (simple, short form, optional, stdin, after `%setup`, outside `%prep`, `%ifarch` Lua, rhel conditional)
- [ ] Decide whether to fix the wrapper (keybox / concatenated armor) based on Phase 1 numbers
