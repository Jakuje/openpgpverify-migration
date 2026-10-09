# Expired keys and SHA-1 key bindings in openpgpverify

Investigation for [rhbz#2532553](https://bugzilla.redhat.com/show_bug.cgi?id=2532553)
("Consider proper handling of expired signing keys in openpgpverify") and the
Phase 1 pilot regressions. Tested with sequoia-sqv 1.5.0 and sequoia-openpgp
2.4.1, as shipped in rawhide on 2026-10-08.

## Summary

| Problem | Pilot packages | Fixable in openpgpverify (wrapper)? | Other fix |
|---|---|---|---|
| Key expired **after** the signature was made | (package test `expired`) | already works: sqv checks expiry at signature time | – |
| Key in the keyring expired **before** the signature was made; upstream extended it later (stale keyring) | yubikey-manager-qt, cairomm1.16 (bug), getdns | **no**: needs an sqv/sequoia change | refresh the keyring (`scripts/refresh_keys.py`); works for yubikey-manager-qt; cairomm and getdns have no newer key published anywhere |
| SHA-1 in self-signatures / subkey bindings | openssl-pkcs11, mpdscribble, openresolv, getdns | **yes**: own crypto policy (prototype on branch `sha1-bindings-and-hints` in `~/devel/openpgpverify`) | refreshed key (openresolv) |
| SHA-1 data signature, DSA-1024 key, v3 signature | dns-root-data, rsakeyfind | should stay rejected | upstream re-signs, or per-package decision |

## Facts established

1. **sqv already checks expiry at the signature's creation time.** The package's
   own `expired` test (key expired 2 days after signing) passes with no options.
   The expectation in bug comment #1 already holds. Checked with real packages
   by moving sqv's reference time (`--time`) past their keys' expiry:

   | Package | Signed | Signing key expires | sqv now / 2026-12-01 / 2027-06-01 / 2031-01-01 |
   |---|---|---|---|
   | fapolicyd (subkey 7200EB2C…) | 2026-05-20, 2026-08-19 | 2026-11-04 | pass / pass / pass / pass |
   | python-oslo-metrics | 2026-08-24 | 2026-11-16 | pass / pass / pass / pass |
   | pinentry, gnupg2, libgpg-error, libksba | 2025-12 … 2026-08 | 2027-03-15 | pass / pass / pass / pass |
   | libstrophe | 2025-03-13 | 2030-03-17 | pass / pass / pass / pass |

   Controls:
   - `--time 2026-08-01` (before the fapolicyd signature) is rejected with
     "Not live until 2026-08-19", so `--time` really is the evaluation time.
   - `sq --time 2026-12-01 inspect` shows the fapolicyd signing subkey as
     expired, yet the signature still verifies.

   So builds do **not** start failing just because a key expired after the
   release was signed.

   **Confirmed with keys that have already expired** (2026-10-08).
   `scripts/find_expired.py` scanned all 558 macro packages (dist-git clones
   plus only the signature files from the lookaside cache) and compared each
   signature's time with its key's expiry: 59 signatures in 49 packages were
   made by keys that have expired since (`data/expiry-scan.jsonl`). Phase 1
   (gpgverify vs openpgpverify in mock, real clock) on 16 of them:

   | Package | Signed | Key expired | Phase 1 |
   |---|---|---|---|
   | vali | 2026-01-23 | 2026-04-12 | both pass |
   | mooltipass-udev | 2023-01-12 | 2023-12-30 | both pass |
   | basez | 2019-10-05 | 2024-10-18 | both pass |
   | hiera | 2023-02-08 | 2025-04-06 | both pass |
   | kio-fuse | 2025-10-13 | 2026-06-14 | both pass |
   | i3status | 2024-08-19 | 2025-05-20 | both pass |
   | conflict | 2023-12-10, 2025-09-30 | 2026-01-18 | both pass |
   | ssh-audit | 2020-03-20, 2024-10-15 | 2025-03-19 | both pass |
   | logrotate | 2024-06-01 | 2025-02-14 | both pass |
   | vim-latex | 2018-01-12 | 2023-01-01 | both pass |
   | libmnl | 2022-04-05 | 2024-10-13 | both pass |
   | dbus-glib | 2021-03-26 | 2021-07-01 | both pass |
   | gnulib-l10n | 2024-12-31 | 2025-02-10 | both pass |
   | dbus | 2025-02-27 | 2026-04-17 | both pass |
   | radvd | 2026-05-25 | 2026-07-11 | already uses openpgpverify in rawhide; sqv passes |
   | time | 2018-03-12 | 2021-02-23 | **fails, but not because of expiry** (see below) |

   time: the dist-git keyring has only the 2020-02-24 self-signatures and
   subkey bindings (re-made when upstream extended the expiry). The 2018
   signature predates every binding: *"No binding signature at time
   2018-03-12"*. gpgv ignores binding times. The keyserver copy still has the
   2014 bindings, and the refreshed keyring verifies
   (`refresh_keys.py` → `proposed`). New Phase 1 reason:
   `binding-after-signature`.

   The same scan found 71 signatures in 67 packages made *after* the expiry
   in our keyring copy (stale keyrings). These are the real expiry
   regressions, and they go through the keyring refresh.
2. **The failures are signatures made after the expiry date in our copy of the key.**
   - yubikey-manager-qt: key expired 2020-09-16, signed 2023-02-03
   - cairomm1.16: key expired 2022-09-08, signed 2023-09-27

   gpgv accepts these. Sequoia rejects them, as the RFC requires: signature
   timestamps are not protected, so anyone holding an expired key could
   backdate.
3. **No sqv option helps.** `--time`, `--not-before`/`--not-after` and
   `--policy-as-of` (with Fedora's `"never"` SHA-1 settings) all still fail.
   The library evaluates the key at the signature creation time, whatever the
   reference time is.
4. **sequoia-openpgp skips the cryptographic check for expired keys.**
   `parse/stream.rs` (2.4.1, around lines 2889–2960) checks `valid_cert().alive()`
   and `ka.alive()` *before* `sig.verify_document()`. An expired key yields
   `VerificationError::BadKey`, and the signature is never verified. **A sqv
   patch that just treats an "expired" `BadKey` as good would accept forged
   signatures.**
5. **Refreshing works when upstream published the extension.**
   - yubikey-manager-qt: the key from keys.openpgp.org / keyserver.ubuntu.com /
     WKD expires on 2027-07-14 and sqv accepts it.
   - openresolv: the refreshed key has new non-SHA-1 self-signatures.
   - cairomm1.16, getdns: only the stale copy exists publicly.
6. **SHA-1 bindings can be accepted narrowly.** Changing only
   `sha1.second_preimage_resistance` (the system policy has `"never"`) to
   `"always"` fixes openssl-pkcs11, mpdscribble and openresolv. It still
   rejects SHA-1 data signatures (collision resistance), DSA-1024 and v3
   signatures. Self-signatures cover data chosen by the key owner, so a
   collision attack doesn't apply. That's why Sequoia keeps this as a
   separate category.

## Wrapper prototype (`~/devel/openpgpverify`, branch `sha1-bindings-and-hints`, not pushed)

- Unless `SEQUOIA_CRYPTO_POLICY` is set, write a temporary policy: the system
  `/etc/crypto-policies/back-ends/sequoia.config` with only
  `sha1.second_preimage_resistance = "always"`. If the system file is missing,
  just a `[hash_algorithms]` table with that line.
- On failure, print hints:
  - stale keyring: the exact `sq --home=none network search --output refreshed.asc FPR` command
  - keybox keyring: the `gpg --export` conversion
  - algorithms rejected by the policy: ask upstream to re-sign
- `Requires: coreutils` (mktemp, cat).
- New tests, made with gpg in a throwaway home:
  - `sha1-binding`: RSA-3072 key with SHA-1 self-signatures, SHA-256 data signature → must pass
  - `sha1-signature`: same key, SHA-1 data signature → must fail
  - `stale-keyring`: key expiring 2025-01-12, extended and used to sign on
    2025-03-01, keyring holds the old copy → must fail with the refresh hint

Test suite in mock (rawhide). With the current 2.2-2 package, everything
passes except sha1-binding and stale-keyring (no hint). With the branch, all
20 pass.

**Decision (2026-10-08): not adopted.** The change owner does not want
openpgpverify to accept SHA-1 bindings. Packages with `sha1-cert` go through a
keyring refresh, or else a bug asking upstream to update the key's
self-signatures. The failure hints in the same prototype could still be
split out on their own.

Questions that were open for this part:
- Should the relaxation be on by default (as prototyped), or opt-in per spec
  (a new macro option, visible in the spec)?
- Is "always" right, or a cutoff date (e.g. reject SHA-1 bindings made after
  2023-02-01, as upstream Sequoia's default)? With Fedora's `"never"`, the
  date is compared to the policy time, so a cutoff only works together with
  `--policy-as-of`, which shifts every other cutoff too. "always" is the
  narrower change.

## Accepting expired keys needs an sqv (or sequoia-openpgp) change

Possible designs, from most to least preferred:

1. **Library option** (sequoia-openpgp): a `DetachedVerifierBuilder` /
   `VerifierBuilder` knob, e.g. `ignore_key_expiration(true)`. When the key or
   certificate is not alive *only* because of `Error::Expired` (not
   `NotYetLive`, not revoked, binding valid under the policy, signing-capable),
   the library still runs `verify_document()` and reports success (ideally
   with a flag the caller can print as a warning). sqv exposes it as e.g.
   `--allow-expired-keys`, and openpgpverify passes it. Works for stdin data,
   detached, inline and cleartext. Needs upstream agreement.
2. **sqv-only fallback**: on `BadKey` whose error is `Error::Expired`, sqv
   checks revocation, `for_signing()` and the signature policy itself, then
   re-hashes the data file (`sig.hash_algo().context()?.for_signature(...)`,
   then `Signature::verify_hash`). Only works for detached signatures with a
   re-readable data file. That rules out `--data=-` (15 specs pipe
   decompressed data in) unless sqv buffers stdin to a temporary file.
   Easy to get subtly wrong; it reimplements part of the verifier.
3. **Fallback to gpgv** inside openpgpverify: rejected, since it would bring
   GnuPG and its weaker checks back into source verification.

Bug comment #0 suggests a middle ground: refuse only keys that expired before
the archive's mtime. That doesn't work, because mtimes are as unprotected as
the signature timestamp and are often normalized.

Suggested policy if (1) lands: accept expired-before-signing keys with a loud
warning in the build log. Keep the migration tooling proposing refreshed
keyrings so that packages move to properly valid keys over time.

## Semi-automatic keyring refresh (implemented)

`scripts/refresh_keys.py propose|show|approve|reject` (see the README):
- looks up only the fingerprints already in the keyring;
- keeps only exact matches;
- merges into the existing certificates and checks the set is unchanged;
- keeps the armored/binary format and re-runs sqv on the host;
- writes `work/PKG/refresh/REVIEW.md` with a before/after `sq inspect` diff.

Only approved refreshes are used by `phase1.py` (in the new variant) and go
into PRs. Pilot: yubikey-manager-qt and openresolv `proposed`; getdns,
mpdscribble, openssl-pkcs11 `no-update`.
