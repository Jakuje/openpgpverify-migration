# Verify source signatures with openpgpverify

> **DRAFT, not to be opened yet:** the keyring refresh below still needs a human review (`scripts/refresh_keys.py show knot-resolver`).

This switches the upstream source signature check from a direct GnuPG call (`gpg2`) to `%openpgpverify` (Sequoia `sqv`), as part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify). The spec called GnuPG itself instead of using `%gpgverify`; the check becomes one `%openpgpverify` call with the same keyring, signature and data.

Why `sqv`:

- It is a verifier made for exactly this job: no home directory, trust database or default keyring, so only the keyring in the spec counts.
- It follows the system crypto policy and checks that the signing key was valid and correctly bound when the signature was made.
- It supports the current OpenPGP standard (RFC 9580, including v6 keys and signatures) and post-quantum (ML-DSA) signatures.
- It is the same OpenPGP implementation that rpm uses for package signatures in Fedora.

### Changes

- the GnuPG verification (import the key into a temporary `GNUPGHOME`, then `gpg2 --verify`) is replaced by one `%{openpgpverify}` call with the same key, signature and data; `GPG_CHECK` still switches it
- added `BuildRequires: openpgpverify`; nothing pulls it into the buildroot implicitly (gpgverify comes in via redhat-rpm-config)
- updated `kresd-keyblock.asc` to the current upstream copy from the URL in the spec (see below)
- Release bumped (`1%{?dist}` → `2%{?dist}`) with a changelog entry

### Testing

The current and the changed spec were both run through `rpmbuild -bp` in a clean mock chroot without network access (fedora-rawhide-x86_64). Every call of the verification tool was logged:

| Spec | Verification calls | Result |
|---|---|---|
| current (`gpg2`) | 2 | pass |
| this PR (`%openpgpverify`) | 1 | fails with the keyring in dist-git; **passes with the refreshed keyring** (sqv run directly) |

Tested on 2026-10-26 at dist-git commit `0d4bf2c20be1` with sequoia-sqv 1.5.0-2.fc45.x86_64 (Fedora DEFAULT crypto policy).

### Keyring update

`%openpgpverify` rejected the signature with the keyring in dist-git (key expired before signing), while `gpg2` ignores that. Upstream has updated the key since: the copy at the URL the spec names for it has the same fingerprint(s) and verifies the release with sqv. This PR replaces the file with that copy, byte for byte:

```
curl -fsSL -o kresd-keyblock.asc https://secure.nic.cz/files/knot-resolver/kresd-keyblock.asc
```

Fingerprints (unchanged):

- `3057EE9A448F362D74205A779AB120DA0A76F6DE`
- `B6006460B60A80E782062449E747DF1F9575A3AA`

What changed in the certificate (`sq inspect`):

```diff
--- dist-git/kresd-keyblock.asc
+++ upstream/kresd-keyblock.asc
@@ -1,10 +1,8 @@
       Fingerprint: 3057EE9A448F362D74205A779AB120DA0A76F6DE
-                   Invalid: The primary key is not live: Expired on 2024-03-06T15:32:20Z
-  Expiration time: 2024-03-06 15:32:20 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2030-02-03 23:00:00 UTC (creation time + 7years 10months 29days 3h 51m 40s)
         Key flags: certification, signing
            Subkey: A5170E99CFCA7ED34200C52CCF853D657BD054EC
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2024-03-06T15:32:20Z
-  Expiration time: 2024-03-06 15:32:20 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2030-02-03 23:00:00 UTC (creation time + 7years 10months 29days 3h 51m 40s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Ales Mrazek <ales.mrazek@nic.cz>
       Fingerprint: B6006460B60A80E782062449E747DF1F9575A3AA
@@ -16,5 +14,5 @@
            UserID: Vladimír Čunát (personal) <v@cunat.cz>
            UserID: Vladimír Čunát (work) <vladimir.cunat@nic.cz>
            UserID: Vladimír Čunát <vcunat@gmail.com>
-self-signatures PositiveCertification: 2021-10-13, 2022-03-07
-self-signatures SubkeyBinding: 2021-10-13, 2022-03-07
+self-signatures PositiveCertification: 2016-10-16, 2017-09-21, 2017-09-25, 2017-11-16, 2019-02-24, 2021-10-13, 2022-03-07, 2024-03-04, 2026-02-04
+self-signatures SubkeyBinding: 2021-10-13, 2022-03-07, 2024-03-04, 2026-02-04
```

### Notes

- Rawhide only. Whether to merge it into other branches is up to you; openpgpverify is available in Fedora 43 and later, EPEL 9 and EPEL 10.
- `BuildRequires: gnupg2` is kept: not checked: the changed spec does not get past the signature check. If it was only there for the signature check, it can go too.
- Nothing changes in the built packages, so this doesn't need a build right away; the new check runs with your next build.

### Questions

This is one of the PRs for the Change, tracked in [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619). If something doesn't fit this package, please comment here; I'll update the PR or close it. The scripts that prepared it are at https://github.com/Jakuje/openpgpverify-migration.
