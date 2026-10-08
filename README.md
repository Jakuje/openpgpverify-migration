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
| SHA-1 key bindings | **Not accepted** by openpgpverify. Fix with a keyring refresh, or a bug for upstream. |
| AI disclosure | `Assisted-by:` commit trailer (Fedora AI contributions policy). |

## Known differences between gpgverify and openpgpverify

The command-line interface is the same (long options, `-k/-s/-d` short
options, `--keyrings`, `--data=-` from stdin). Same behaviour for armored,
binary and concatenated-armor keyrings. Differences:

| Case | gpgverify | openpgpverify |
|---|---|---|
| GnuPG keybox (`.kbx`, usually named `*.gpg`) keyring | pass | **fail** |
| SHA-1 in the key's own self-signatures / subkey bindings (`sha1-cert`) | pass | **fail** |
| SHA-1 data signature (`sha1-sig`) | pass | **fail** |
| OpenPGP v3 signature packet (`v3-sig`, rejected since 2021) | pass | **fail** |
| Key expired before the signature was made (`expired`, often a stale keyring copy) | **pass** | fail |
| Several armored blocks in one signature file | pass | **fail** |
| Exit code for "no matching key" | 2 | 1 |
| stdout | quiet | prints fingerprint |
| `--output` | inline or cleartext | cleartext only, refuses to overwrite (only git-lfs uses it) |

The result depends on the Sequoia crypto policy, so the harness runs with the
system DEFAULT policy and records it (no `SEQUOIA_CRYPTO_POLICY` override).

gpgv accepts a signature made by a key that had already expired according to
the keyring (yubikey-manager-qt: key expired 2020-09, tarball signed 2023-02).
Sequoia rejects it. Usually upstream extended the expiry and the dist-git
copy is stale.

**Buildroot:** `gnupg2` is in every rawhide buildroot (`rpm-build` →
`rpm-sign-libs` requires `/usr/bin/gpg2`), and `redhat-rpm-config` adds
`gpgverify` through `(gpgverify if gnupg2)`. That is why specs without any gpg
BR work today. `openpgpverify` is *not* in the default buildroot, so a
missing BR shows up in testing. Dropping `BR: gnupg2` changes nothing until
rpm stops depending on gpg.

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
1. **Side-by-side test** (`scripts/phase1.py`): for each in-scope package,
   at rawhide HEAD:
   1. Anonymous dist-git clone into `work/PKG/dist-git`, then
      `fedpkg sources`. Re-classify the current spec and convert it
      (`scripts/convert.py`).
   2. In one fresh mock chroot without network (`fedora-rawhide-x86_64`, plus
      `fedora-eln-x86_64` with `--eln` for specs mentioning RHEL):
      - `--installdeps` the new spec, then `rpmbuild -bp --nodeps`;
      - `--installdeps` the unchanged spec, then `rpmbuild -bp --nodeps`.

      Specs that verify outside `%prep` use `-bc`. Running the whole stage
      covers stdin pipes, verification after `%setup`, per-arch Lua source
      selection and `%{_sourcedir}` paths. Specs are untrusted code (`%(…)`,
      `%{lua:}`), so they are only parsed and run inside mock.
   3. **Call log**: inside the chroot, `/usr/libexec/{gpgverify,openpgpverify}`
      (and `gpg`/`gpgv` for raw-verify packages) are replaced by wrappers
      that log the arguments and exit code of every call, then run the real
      tool. This gives an exact per-call record.
   4. **Guard against verification that silently disappears**: the unchanged
      spec must make at least one gpgverify call, and the new one the same
      number of openpgpverify calls and no gpgverify calls. Tested for real:
      getdns with the added BR removed → `guard-failed (old ran 1 verify
      calls, new ran 0)`.
   5. Outcomes:
      - `both-pass` (status `tested`)
      - `regression`: diagnosed with the keyring format (keybox magic), armor
        block count, `sq inspect` of the keyring and the hash algorithm from
        `sq packet dump` of the signature. Reasons: `sha1-cert`, `sha1-sig`,
        `v3-sig`, `expired`, `binding-after-signature`, `keybox`,
        `concatenated-armor`, `policy`, `unknown`.
      - `both-fail`: the package was already broken; reported separately
      - `guard-failed`: verify call counts don't match
      - `not-buildable`: the unchanged spec can't install its deps in that
        chroot (only rawhide counts toward the status)
      - `manual`: raw gpg verification or an unconvertible spec; only the
        baseline is run
      - `error`: a harness, clone or sources problem
   6. `scripts/report.py` renders the state file to Markdown
      (`reports/phase1-*.md`).
1b. **Keyring refresh for regressions** (`scripts/refresh_keys.py`),
   semi-automatic, with a manual review for each package:
   - `propose [PKG...]` (default: regressions with reason `expired`,
     `sha1-cert`, `policy` or `unknown`): looks up only the fingerprints
     already in the keyring (keyservers + WKD via `sq network search`) and
     keeps only exact matches. It merges them into the existing certificates,
     checks the set of certificates is unchanged, keeps the armored/binary
     format and re-runs sqv on the host. Writes `work/PKG/refresh/FILE` and
     `REVIEW.md` (a before/after `sq inspect` diff). Results: `proposed`,
     `no-update`, `not-found`, `still-fails`.
   - `show PKG`, then `approve PKG [--note]` or `reject PKG --note`. Only
     `proposed` can be approved, and the reviewer and time are recorded.
   - `phase1.py PKG` then uses approved keyrings in the new variant only
     (`keyring_refresh_applied`). The PR will include the refreshed keyring.

   `scripts/find_expired.py` finds stale keyrings (and keys that expired
   after signing) for all packages in minutes, without downloading sources:
   dist-git clones plus signature files from the lookaside cache only.

   Background, and what can and can't be fixed in openpgpverify itself:
   [docs/expired-keys-and-sha1.md](docs/expired-keys-and-sha1.md).
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
- [x] Seed `data/state/packages.jsonl` from the inventory (`scripts/seed_state.py`, maintainers from `pagure_owner_alias.json`)
- [x] Phase 1 harness and pilot (19 packages, `reports/phase1-pilot.md`)
- [ ] Phase 1 on all in-scope packages
- [x] Semi-automatic keyring refresh with per-package review (`scripts/refresh_keys.py`)
- [x] openpgpverify prototype: SHA-1 key bindings accepted + failure hints (local branch `sha1-bindings-and-hints` in `~/devel/openpgpverify`, tests pass in mock)
- [x] Decided: no SHA-1 binding relaxation in openpgpverify
- [x] Confirmed with real keys: signatures made while the key was valid keep verifying after it expires (`scripts/find_expired.py` scan of 558 packages + Phase 1 on 16 with already-expired keys: 14 pass, radvd already converted, time fails for a binding-history reason)
- [ ] Expired-before-signing keys: discuss the library/sqv option with Sequoia upstream (docs/expired-keys-and-sha1.md)
- [ ] Review the proposed keyring refreshes (yubikey-manager-qt, openresolv)
