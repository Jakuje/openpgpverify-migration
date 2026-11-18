# Process and tooling

How packages are found, tested, converted and followed up. The goal and the
current status are in the [README](../README.md).

## Daily status update

```
D=$(date +%F); S=data/snapshots/$D
mkdir -p $S/rpm-specs
curl -sSfL -o $S/rpm-specs.tar.xz https://src.fedoraproject.org/lookaside/rpm-specs-latest.tar.xz
curl -sSfL -o $S/pagure_owner_alias.json https://src.fedoraproject.org/extras/pagure_owner_alias.json
tar -xJf $S/rpm-specs.tar.xz -C $S/rpm-specs --strip-components=1
ln -sfn $D data/snapshots/latest

python3 scripts/classify.py data/snapshots/latest/rpm-specs data/inventory/inventory-$D.jsonl
python3 scripts/progress.py data/inventory/inventory-2026-10-06.jsonl data/inventory/inventory-$D.jsonl \
    reports/progress-$D.md --prs data/prs-$D.tsv --fetch --since PREV_INVENTORY PREV_PRS
python3 scripts/sync_state.py data/inventory/inventory-$D.jsonl data/prs-$D.tsv --write
python3 scripts/eln_report.py data/inventory/inventory-$D.jsonl data/prs-$D.tsv reports/eln-$D.md
```

Only the tarball of older snapshots is kept (the extracted specs take about
220 MB). New bug comments are recorded with `scripts/bug_response.py`.

## Phases

0. **Inventory** (`scripts/classify.py`): scan the daily all-specs tarball
   as text, cross-checked against the rawhide source repo.
   `scripts/seed_state.py` creates or refreshes the state records from it,
   with the maintainers from `pagure_owner_alias.json`.
1. **Side-by-side test** (`scripts/phase1.py`): for each in-scope package,
   at rawhide HEAD:
   1. Anonymous dist-git clone into `work/PKG/dist-git`, then
      `fedpkg sources`. Re-classify the current spec and convert it
      (`scripts/convert.py`, rules below).
   2. In one fresh mock chroot without network (`fedora-rawhide-x86_64`, plus
      `fedora-eln-x86_64` with `--eln` for specs with `%{?rhel}` conditionals):
      - `--installdeps` the new spec, then `rpmbuild -bp --nodeps`;
      - `--installdeps` the unchanged spec, then `rpmbuild -bp --nodeps`.

      Specs that verify outside `%prep` use `-bc`. Running the whole stage
      covers stdin pipes, verification after `%setup`, per-arch Lua source
      selection and `%{_sourcedir}` paths. Specs are untrusted code (`%(…)`,
      `%{lua:}`), so they are only parsed and run inside mock.

      `--verify-only` installs only the verification tools and stops `%prep`
      right after the signature check, for packages whose sources are too
      large to unpack on the test machine (qemu). Even that needs the sources
      about twice; libreoffice (590 MB of sources) was converted by hand,
      checked with sqv on the host, and its PR CI build is the test.
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
        `v3-sig`, `weak-key`, `unparseable-cert`, `expired`,
        `binding-after-signature`, `keybox`, `concatenated-armor`, `policy`,
        `unknown`.
      - `both-fail`: the package was already broken; reported separately
      - `guard-failed`: verify call counts don't match
      - `not-buildable`: the unchanged spec can't install its deps in that
        chroot (only rawhide counts toward the status)
      - `not-verified`: a secondary chroot (ELN) where even the unchanged spec
        doesn't verify (e.g. bind verifies only `%if 0%{?fedora}`); doesn't
        affect the status
      - `manual`: raw gpg verification or an unconvertible spec; only the
        baseline is run
      - `error`: a harness, clone or sources problem
   6. Reports: `scripts/report.py` renders the state file
      (`reports/phase1-*.md`); `scripts/progress.py` compares the starting
      snapshot (2026-10-06) with today's inventory and the dist-git PRs
      (`reports/progress-DATE.md`); `scripts/eln_report.py` lists the ELN
      packages (`reports/eln-DATE.md`).
   7. `scripts/sync_state.py INVENTORY PRS --write` feeds the inventory and the
      PR list back into the state file: PRs opened by hand get recorded
      (`pr_url`, `existing_prs`) and packages converted in rawhide become
      `superseded`. Run it after every `progress.py --fetch`.

   Harness notes (an 18 GB, 2-CPU machine):
   - one mock root per parallel job (`--uniqueext opv-N`), reused; per-package
     roots left a 200 MB bootstrap each; `--jobs 2` at most;
   - `--prune-sources` removes downloaded sources of passing packages, and
     `--min-free-gb` keeps a package from starting on a full disk; the dnf
     cache is scrubbed every 20 packages;
   - if `--installdeps` on a spec fails (specs that `%load` files from their
     sources, like emacs and llvm), the BuildRequires come from an SRPM built
     with the sources;
   - specs with `%autorelease` are never bumped, also with a guarded
     `%{?autochangelog}`.
1b. **Keyring refresh for regressions** (`scripts/refresh_keys.py`),
   semi-automatic, with a manual review for each package:
   - `propose-upstream [PKG...]` (preferred): downloads the keyring from the
     URL the spec names for it (`Source:` URL or a URL in the comment above),
     and keeps it only if it has exactly the same fingerprints, differs from
     dist-git and makes sqv pass. The file is used byte for byte
     (`curl -o FILE URL`). `--url URL` (and `--signature-url URL`) take the
     key (and signature) from a URL upstream pointed to instead; that URL is
     then added to the comment above the keyring's `Source` line. Reviews in
     `reports/keyring-upstream/`.
   - `propose [PKG...]`: replaces the keyring with what the keyservers have for
     the fingerprints already in it (`sq network keyserver search`, armored),
     checks the set of certificates is unchanged and re-runs sqv on the host.
     A GnuPG keybox, which sqv cannot read, is exported with gpg (data only,
     on the host) to read its fingerprints and always counts as changed.
   - `propose-convert --signers FPR... [--new-name FILE]`: a keyring with only
     the release signer's key, for large shared keyrings (e.g. the GNU
     keyring) that are stale or too big to move into git.
   - Each proposal writes `work/PKG/refresh/FILE` and `REVIEW.md` (a
     before/after `sq inspect` diff). Results: `proposed`, `no-update`,
     `not-found`, `still-fails`.
   - `show PKG`, then `approve PKG [--note]` or `reject PKG --note`. Only
     `proposed` can be approved, and the reviewer and time are recorded.
     Nothing is approved without the reviewer.
   - `phase1.py PKG` then uses approved keyrings in the new variant only
     (`keyring_refresh_applied`), and puts the refresh command in the comment
     above the keyring's `Source` line.
   - In the PR, a keyring update is its own first commit (maintainers asked
     for that), followed by the openpgpverify commit. A keyring stored in the
     lookaside cache moves into git, because a PR cannot upload there.

   `scripts/find_expired.py` finds stale keyrings (and keys that expired
   after signing) for all packages in minutes, without downloading sources.
   `scripts/upsort.py` sorts proposed refreshes by where a current upstream
   copy of the key can be fetched.
2. **Proposals** (`scripts/render_proposals.py PKG...`): renders what each
   maintainer gets into `proposals/PKG/`. It doesn't re-convert anything: it
   uses the spec that Phase 1 tested, at the tested dist-git commit, and
   refuses if dist-git changed since.
   - **PR**: `000N-*.patch` (`git format-patch` of the commits, made in a
     scratch clone, including any approved keyring refresh and the changelog
     entry for specs without `%autochangelog`) and `PR.md` (title +
     description from `templates/pr-description.md`).
   - **bug**: `BUG.md` (Bugzilla fields + text from `templates/bug.md`, with
     the reason explained and the fix options). sqv reports only the first
     problem, so `scripts/bug_diag.py check` lists all of them (signature,
     key algorithm, self-signature hashes, expiry, network copy) and
     `bug_diag.py apply` picks the bug text from that (`bug_reason`,
     `bug_findings` in the state). `scripts/bug_groups.py` groups the bugs by
     upstream signing key and by Fedora owner (`reports/bug-groups-*.md`);
     `scripts/file_bugs.py` files them, blocking rhbz#2569052.
   - `proposals/README.md`: an index.

   Commit message: `templates/commit-message.txt`, with an `Assisted-by:`
   trailer. The claims in the PR text were checked on Fedora 44 (sequoia-sqv
   1.5.0): sqv verifies a v6 (RFC 9580) signature made with an
   ML-DSA-65+Ed25519 key, and rpm links `librpm_sequoia`.
3. **Rollout**: pilot on our own packages, a heads-up mail to the
   devel list, then PRs in batches (`scripts/ready_list.py` lists the
   ready ones and checks that dist-git is still at the tested commit;
   `scripts/open_prs.py` can open them from a fork, though PRs are now opened
   by hand). Bugs for regressions that need upstream action. After a fixed
   period without a response, a provenpackager merges, pointing to the
   approved Change.

## Conversion rules

1. **Macro call**: keep the existing form exactly.
   - `%{gpgverify}` → `%{openpgpverify}`
   - `%gpgverify -k2 -s1 -d0` → `%openpgpverify -k2 -s1 -d0`
   - `%{?gpgverify:…}` → `%{?openpgpverify:…}`

   Never drop the braces: `%gpgverify --keyring=…` fails with *Unknown
   option -*. Escaped `%%gpgverify` (comments) is left alone.
2. **Always add `BuildRequires: openpgpverify`.** Most specs get gpgverify
   implicitly through `redhat-rpm-config`'s `Requires: (gpgverify if gnupg2)`;
   nothing pulls in openpgpverify that way.
3. **`BR: gpgverify`, `%{_bindir}/gpgv2`, `%{gpgverify}`**: drop them.
   **`BR: gnupg2`** (or `BR: gpg`): with `keep` (other gpg use in the spec) it
   stays. With `remove` (no other gpg use, no `%check`) or `review` (has
   `%check`), it is dropped only if the **gnupg2 check** in Phase 1 passes:
   gnupg2 is in every buildroot, so a normal build proves nothing. Instead,
   all `gnupg2*` packages and gpgverify are removed from the chroot with
   `rpm -e --nodeps`, and the changed spec is built completely (`rpmbuild -bb`,
   `%check` included, 2 h limit). The BR is dropped only if that build
   passes and neither the build log nor test files in the unpacked sources
   mention gpg (tests often skip silently without it). If the build fails,
   it is repeated with gnupg2 installed to tell "needs gpg" from an existing
   FTBFS. In all other cases the BR is kept and the PR says why
   (`gnupg2_check` in the state). A re-run reuses a passed check when dist-git
   is still at the commit it ran on.
4. **Release / changelog**: specs with `%autochangelog` get nothing extra
   (the commit subject becomes the changelog line). The others get a Release
   bump and a changelog entry from `rpmdev-bumpspec`, run inside the Phase 1
   mock chroot before `%prep`, so the tested spec is exactly the proposed one.
5. **Raw gpg/gpgv calls** (`raw-verify`) are first turned into a
   `%{gpgverify}` call and then converted like any other spec. The simple form
   `[CMD |] gpgv[2] [--quiet] --keyring K SIG DATA` is rewritten by
   `convert.rewrite_raw()` (`--data=-` when the data is piped in). Anything
   else (temporary GNUPGHOME, `gpg --import`/`--dearmor`, `||` between keys)
   has a hand-written `manual/PKG.patch` plus `manual/PKG.md` with the PR
   bullet. Raw calls in the `%else` of a Fedora condition (old EL branches)
   stay. Phase 1 keeps `gpg`/`gpgv` wrapped in both runs, so a leftover GnuPG
   call in the new spec fails the guard.
6. **RHEL conditionals**: openpgpverify is available in Fedora 43+, ELN, EPEL 9
   and EPEL 10 (not EPEL 8), so specs with `%{?rhel}` conditionals get the
   plain conversion too. A gpg BuildRequires inside a conditional is dropped
   and `BuildRequires: openpgpverify` is added unconditionally; a `%else`
   branch or `%if` block that contained only that BuildRequires is removed.
   The PR text mentions EPEL 8 for these specs.

   Exception: a `%if COND` block that held only the gpg BuildRequires, where
   the same `%if COND` also guards the call in `%prep` (OpenStack's
   `%if 0%{?sources_gpg} == 1`), keeps its condition and gets
   `BuildRequires: openpgpverify` in place of the dropped line.
7. **Where `BuildRequires: openpgpverify` goes**, first match: in place of a
   dropped unconditional gpg BuildRequires; inside the `%if` block from rule
   6; right after a kept `BR: gnupg2`; at its alphabetical position in the
   longest run of unconditional BuildRequires if that run is sorted (one
   entry out of order, or up to 10 %, is tolerated); otherwise after the last
   unconditional BuildRequires. It copies the `BuildRequires:` spacing of the
   line next to it.

## ELN

ELN packages go first ([eln#610](https://github.com/fedora-eln/eln/issues/610)).
`data/eln-in-scope.txt` lists the in-scope packages from the content
resolver's ELN workload and buildroot source lists (164 as of 2026-10-12).
All of them were tested in rawhide, plus ELN for specs with `%{?rhel}`
conditionals. `scripts/eln_report.py` writes the per-package report linked
from the status comments on the issue (drafts in `announce/`).

## Announcement

The migration is part of the approved Change, so instead of the FESCo mass
package change process there was a heads-up mail to the devel list.
`announce/devel-mail.txt` was its draft (prepared for the mass change policy
at first). `scripts/announce_lists.py` writes package lists by name and by
maintainer (`announce/packages-by-name.txt`,
`announce/packages-by-maintainer.txt`).
