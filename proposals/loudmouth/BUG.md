Product: Fedora
Component: loudmouth
Version: rawhide
Blocks: 2569052
Summary: loudmouth: source signature does not verify with openpgpverify (signing key algorithm rejected)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For loudmouth, the switch can't be done in a simple PR: the current check with `gpgv` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `52d8aef38f55`):

```
%openpgpverify --keyring=gpgkey-EACADFF156849BC89653139E3C2900DEACB7FC95.gpg --signature=loudmouth-1.5.4.tar.bz2.asc --data=loudmouth-1.5.4.tar.bz2
```

```
Signing key on EACADFF156849BC89653139E3C2900DEACB7FC95 is not bound:
           No binding signature at time 2021-01-25T20:22:45Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

The release signature (SHA-1, made 2021-01-25) is by the key `EACADFF156849BC89653139E3C2900DEACB7FC95` (DSA 1024 bits). sqv reports only the first problem it hits (above). All the problems found:

- The key is DSA-1024. DSA keys and RSA keys shorter than 2048 bits are no longer considered secure, and the crypto policy rejects them. DSA-1024 can only use 160-bit hashes, which is also why its signatures are SHA-1.
- The self-signatures that bind the key's user IDs to it use only SHA-1. SHA-1 is no longer considered secure: collisions have been practical since 2017 (SHAttered) and chosen-prefix collisions since 2020 (SHA-1 is a Shambles), and the crypto policy rejects it. GnuPG doesn't check self-signatures; Sequoia does, and without a valid one it doesn't use the key at all.
- The key expired on 2015-10-21, before the release was signed on 2021-01-25, according to the keyring in dist-git. GnuPG ignores expiry; Sequoia checks that the key was valid when the signature was made.
- The release signature itself uses SHA-1 too; for signatures over data, this won't be relaxed.

The copy of the key on keys.openpgp.org, keyserver.ubuntu.com and WKD is newer, but its problems remain: key algorithm rejected by the crypto policy, the key's self-signatures use only SHA-1.

### What can be done

- Ask upstream to create a new key (for example Ed25519 or RSA 3072+), publish it, and sign releases with it using SHA-256 or better. Then switch the keyring to it.
- Until then the package can keep the current GnuPG check, or verify the tarball differently (for example against a checksum published over HTTPS).

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change replaces the direct GnuPG call with one `%{openpgpverify}` call (same keyring, signature and data) and adds `BuildRequires: openpgpverify`; it is ready and tested up to the signature check. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
