# Data

## Starting inventory (2026-10-06)

```
python3 -I scripts/classify.py data/snapshots/latest/rpm-specs \
    data/inventory/inventory-2026-10-06.jsonl data/snapshots/latest/rawhide-srpm-sizes.txt
```

| Category | Packages | Notes |
|---|---|---|
| `macro-simple` | 425 | `%prep` call(s) with `%{SOURCEn}` args only, no `%if`, no pipe, before `%setup` |
| `macro-complex` | 133 | everything else using the macro |
| `raw-verify` | 36 | direct `gpgv2`/`gpg --verify` (openssh, qemu, libreoffice, samba family, …); converted by hand |
| **in scope** | **594** | about 4.9 GB of sources |
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

## State record (`data/state/packages.jsonl`)

The single mutable source of truth: one record per in-scope package, created
from the inventory (`scripts/seed_state.py`) and updated by every later step,
so steps can be resumed and re-run. The main fields:

- `status`: `inventory` (not tested), `tested` (converted spec passes),
  `regression`, `both-fail`, `guard-failed`, `not-buildable`, `manual`,
  `error`, `skipped` (retired, or out of scope by now), `superseded`
  (converted in rawhide, by our PR or otherwise)
- `outcome_detail`, `results` (per-chroot call logs), `spec_commit`,
  `tested_at`, `harness_version`, `convert_notes`, `gnupg2_check`
- `keyring_refresh` (proposal, review and approval), `keyring_refresh_applied`
- `pr_url`, `existing_prs` (PRs by others)
- `bug_id`, `bug_reason`, `bug_findings`, `bug_response` (latest reply,
  older ones in `bug_response_history`)
- `note`: free text for anything else (PR comments, hand-made patches)

`scripts/state.py` has `load()`/`save()`.
