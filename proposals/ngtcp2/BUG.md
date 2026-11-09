Product: Fedora
Component: ngtcp2
Version: rawhide
Blocks: 2523619
Summary: ngtcp2: source signature does not verify with openpgpverify (signing key algorithm rejected)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For ngtcp2, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `21d2911187d9`):

```
%openpgpverify --keyring=tatsuhiro-t.asc --signature=ngtcp2-1.25.0.tar.xz.asc --data=ngtcp2-1.25.0.tar.xz
```

```
Signing key on F4F3B91474D1EB29889BD0EF7E8403D5D673C366 is not bound:
           primary key
  because: No binding signature at time 2026-07-26T08:28:54Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

Checked in full, not only the first error sqv reports: the release signature (v4, SHA-512, made 2026-07-26) is by signing subkey 516B622918D15C478AB1EA3A5339A2BE82E07DEC (RSA 4096 bits) of key F4F3B91474D1EB29889BD0EF7E8403D5D673C366 (DSA 1024 bits). The key in dist-git: key algorithm rejected by the crypto policy (primary key DSA-1024); the key's self-signatures use only SHA-1. The copy on keyservers/WKD has the same problems.

The release is signed with a key whose algorithm the crypto policy rejects (DSA, or RSA shorter than 2048 bits); for a signing subkey, its primary key counts too. Neither a new release signature nor new self-signatures with this key will help. (DSA-1024 can only use 160-bit hashes, which is also why such signatures are SHA-1.)

### What can be done

- Ask upstream to create a new key (for example Ed25519 or RSA 3072+), publish it, and sign releases with it using SHA-256 or better. Then switch the keyring to it.
- Until then the package can keep `%gpgverify`, or verify the tarball differently (for example against a checksum published over HTTPS).

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
