Product: Fedora
Component: aeskeyfind
Version: rawhide
Blocks: 2523619
Summary: aeskeyfind: source signature does not verify with openpgpverify (signing key algorithm rejected)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For aeskeyfind, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `5ec5547ba5ee`):

```
%openpgpverify --keyring=gpgkey-12E404FFD3C931F934052D06B8841A919D0FACE4.gpg --signature=aeskeyfind-1.0.tar.gz.asc --data=aeskeyfind-1.0.tar.gz
```

```
Error: Policy rejected packet type

Caused by:
    Signature Packet v3 is not considered secure since 2021-02-01T00:00:00Z
openpgpverify: Signature verification failed.
```

### Why

Checked in full, not only the first error sqv reports: the release signature (v3, SHA-1, made 2008-07-18) is by key 12E404FFD3C931F934052D06B8841A919D0FACE4 (DSA 1024 bits). The signature itself is rejected: it is in the version 3 format and it uses SHA-1. The key in dist-git: key algorithm rejected by the crypto policy (DSA-1024); the key has no self-signature from before the release signature. The copy on keyservers/WKD still has: key algorithm rejected by the crypto policy (DSA-1024); the key's self-signatures use only SHA-1.

The release is signed with a key whose algorithm the crypto policy rejects (DSA, or RSA shorter than 2048 bits); for a signing subkey, its primary key counts too. Neither a new release signature nor new self-signatures with this key will help. (DSA-1024 can only use 160-bit hashes, which is also why such signatures are SHA-1.)

### What can be done

- Ask upstream to create a new key (for example Ed25519 or RSA 3072+), publish it, and sign releases with it using SHA-256 or better. Then switch the keyring to it.
- Until then the package can keep `%gpgverify`, or verify the tarball differently (for example against a checksum published over HTTPS).

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
