# Next steps as of 2026-11-03

Status: [progress-2026-11-03.md](progress-2026-11-03.md). Of the 594 packages that verified sources with GnuPG on 2026-10-06:

- 121 are converted (20 %);
- 139 have an open PR (23 %), 137 of them ours;
- 330 are still to do.

For ELN (164 packages): 64 converted, 26 open PRs, 72 to do.

What is left, and the proposed order:

## 1. Rich's packages: keyring update only (9 packages, 8 in ELN)

Rich re-signed his key with backdated SHA-256 bindings and put it in libguestfs and virt-v2v as `rich@annexia.org-pubkey.txt`. These packages still carry the old `libguestfs.keyring`, which fails on SHA-1. With the new key, `sqv` verifies their current release; checked on the host for all nine:

hivex, libnbd, nbdkit, ocaml-augeas, qemu-sanity-check, supermin, virt-p2v, virt-top, virt-what

All but qemu-sanity-check are ELN packages. Proposal: ask Rich whether he wants to swap the keyring himself, or let us open PRs that copy the key from libguestfs and convert to `%openpgpverify` in the same PR (each needs a Phase 1 run with the new keyring first).

## 2. Bugs for upstream/maintainer action (130 packages, 39 in ELN)

The drafts are in `proposals/*/BUG.md`, with the backdated re-signing advice from the Red Hat blog article. No bug has been filed yet. Rich's case shows the advice works, which was the open question.

By reason:

| Reason | Packages | What fixes it |
|---|---|---|
| `sha1-cert` | 58 | upstream re-signs the key bindings with SHA-256, backdated |
| `sha1-sig` | 31 | upstream re-signs the release, or the next release is signed with SHA-256 |
| `weak-key` | 12 | upstream needs a new key (DSA/RSA-1024) |
| `unparseable-cert` | 9 | broken or ancient keyring; a new export from upstream |
| `expired` | 9 | key expiry extended, backdated if the release predates it |
| `v3-sig` | 8 | upstream re-signs (v3 signatures) |
| `binding-after-signature` | 2 | older self-signatures are needed in the keyring |
| `concatenated-armor` | 1 | tor; split or re-armor the keyring |

Proposal: file the 39 ELN bugs first (minus the 8 Rich packages from step 1), then the rest in batches of about 30. A bug goes to the Fedora maintainer, who forwards it upstream. Before each batch, re-check that the package is unchanged in dist-git. Separately: rust, qemu, libreoffice and clang15 are handled by hand.

## 3. Keyring refresh proposals awaiting review (98 packages, 29 in ELN)

The keyserver copy of the same fingerprints fixes the check (46 `expired`, 44 `sha1-cert`, 4 keybox, 2 `sha1-sig`, 2 `binding-after-signature`). They need your review of the before/after `sq inspect` in `reports/keyring-refresh/`. Proposal: review the 29 ELN ones first; once approved, phase1.py re-runs with the refreshed keyring and they join the ready list as a two-commit PR.

## 4. Remaining ready PRs (98 packages, 3 in ELN)

- About 70 never had `BuildRequires: gnupg2`, so the patch only swaps the BR and the macro. These are low risk and can be opened in batches like today's.
- 28 keep gnupg2, and the PR text says why (tests need gpg, sources too large to check, or the package does not build at all). Worth a quick look before opening.
- The ELN ones (libguestfs, virt-v2v, guestfs-tools) can go first.

## 5. Follow-ups on open PRs

- **No reply for over a week (14):** SDL3#4, autoconf-archive#8, bc#9, crun#159, ldns#10, libmnl#4, libnetfilter_conntrack#4, libssh2#4, libxcrypt#23, lttng-ust#3, man-db#22, mdadm#14, pcre2#39, squid#10. A friendly ping. pcre2#39 has an LGTM, and libxcrypt#23 is waiting for someone with merge rights.
- **ethtool#9:** conflicts with a newer dist-git commit; the rebased change passes. It needs a push to the PR branch, so it waits for your go-ahead.
- **Robert's question on Fedora < 45 and EPEL:**
  - libidn2#2: no active EPEL branch, so no `%if` is needed. A follow-up may unblock it.
  - ethtool#9: Fedora only, so no `%if` is needed.
  - rpki-client#2: has epel8, so it needs a fallback.

## 6. Manual cases

| Package | State |
|---|---|
| bind | the check is disabled in the spec |
| python-gnocchiclient | `%gpgverify` never runs (guard-failed) |
| tinygo | rawhide is missing golang(github.com/mailru/easyjson) |
| libreoffice | too large for the test machine; by hand |

## Later phases

- 46 packages with `BuildRequires: gnupg2` but no verification: is the BR still needed?
- 211 packages ship `.asc`/`.sig` sources but never verify them: add `%openpgpverify`.
