# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show pyparted`).

This switches the upstream source signature check from a direct GnuPG call (`gpg`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The spec called GnuPG itself instead of using `%gpgverify`; the check becomes one `%openpgpverify` call with the same keyring, signature and data.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- the `gpg --verify` call with its own keyring and trust database is replaced by `%{openpgpverify}` with the same keyring, signature and data. sqv does not use a trust database, so `trustdb.gpg` (Source3) is no longer needed; it is left in place here and can be removed together with the file
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- refreshed keyring `keyring.gpg` (see below); the comment above its `Source` line now shows the commands for refreshing it
- Release bumped (`17%{?dist}` → `18%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`gpg`) | 1 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-26 at dist-git commit `f00b886f17ce` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring refresh

`%openpgpverify` cannot read the keyring in dist-git: it is a GnuPG keybox, which `gpg` reads but sqv does not, so it is exported to a plain OpenPGP keyring. The same certificate, looked up by fingerprint (hkps://keyserver.ubuntu.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com), has self-signatures our copy is missing (a renewed expiry, modern hashes or the older binding history), so this PR updates the keyring. No key was added or removed. Please check the fingerprint against upstream:

- `08F7C8B3C621950C138F766162977BB9C841B965`

The refresh, as run (the spec comment above the `Source` line has the same commands without the one-time keybox export, for the next refresh):

```
gpg --homedir "$(mktemp -d)" --batch --no-default-keyring --keyring ./keyring.gpg --export --output keyring.gpg.pgp
sq --home=none network search --output - 08F7C8B3C621950C138F766162977BB9C841B965 \
  | sq keyring filter --experimental --cert 08F7C8B3C621950C138F766162977BB9C841B965 --output update.pgp
sq keyring merge keyring.gpg.pgp update.pgp | sq packet dearmor --output keyring.gpg.new
mv keyring.gpg.new keyring.gpg
```

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/keyring.gpg (exported from keybox)
+++ refreshed/keyring.gpg
@@ -8,3 +8,4 @@
            UserID: David Lawrence Cantrell, Jr. <dcantrell@redhat.com>
 self-signatures PositiveCertification: 2019-10-14
 self-signatures SubkeyBinding: 2019-10-14
+third-party GenericCertification: 1
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the changed spec does not get past the signature check. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
