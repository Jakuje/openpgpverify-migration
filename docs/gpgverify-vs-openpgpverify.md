# Differences between gpgverify and openpgpverify

The command-line interface is the same (long options, `-k/-s/-d` short
options, `--keyrings`, `--data=-` from stdin). Same behaviour for armored,
binary and concatenated-armor keyrings. Differences:

| Case | gpgverify | openpgpverify |
|---|---|---|
| GnuPG keybox (`.kbx`, usually named `*.gpg`) keyring | pass | **fail** |
| SHA-1 in the key's own self-signatures / subkey bindings (`sha1-cert`) | pass | **fail** |
| SHA-1 data signature (`sha1-sig`) | pass | **fail** |
| DSA key (`weak-key`) | pass | **fail** |
| Keyring with an old v3 (PGP 2) key (`unparseable-cert`; gpgv skips the key, sqv rejects the whole file) | pass | **fail** |
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
copy is stale. Signatures made while the key was valid keep verifying after
it expires (checked with `scripts/find_expired.py` on 558 packages and Phase 1
on 16 packages with already-expired keys). More background, and what can and
can't be fixed in openpgpverify itself:
[expired-keys-and-sha1.md](expired-keys-and-sha1.md).

## Buildroot

`gnupg2` is in every rawhide buildroot (`rpm-build` → `rpm-sign-libs`
requires `/usr/bin/gpg2`), and `redhat-rpm-config` adds `gpgverify` through
`(gpgverify if gnupg2)`. That is why specs without any gpg BR work today.
`openpgpverify` is *not* in the default buildroot, so a missing BR shows up in
testing. Dropping `BR: gnupg2` changes nothing until rpm stops depending on
gpg.
