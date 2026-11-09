Product: Fedora
Component: oclock
Version: rawhide
Blocks: 2523619
Summary: oclock: source signature does not verify with openpgpverify (signing key algorithm rejected)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For oclock, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `ce90329951a3`):

```
%openpgpverify --keyring=oclock.gpg --signature=oclock-1.0.6.tar.xz.sig --data=oclock-1.0.6.tar.xz
```

```
Signing key on 4A193C06D35E7C670FA4EF0BA2FB9E081F2D130E is not bound:
           primary key
  because: Policy rejected asymmetric algorithm
  because: DSA1024 is not considered secure
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

Checked in full, not only the first error sqv reports: the release signature (v4, SHA-512, made 2024-12-04) is by signing subkey 2F7DBCAD5B30E668BBD516C1CFDF148828C642A7 (RSA 4096 bits) of key 4A193C06D35E7C670FA4EF0BA2FB9E081F2D130E (DSA 1024 bits). The key in dist-git: key algorithm rejected by the crypto policy (primary key DSA-1024); the key had expired when the release was signed (on 2022-07-21); the key has no self-signature from before the release signature. The copy on keyservers/WKD still has: key algorithm rejected by the crypto policy (primary key DSA-1024).

The release is signed with a key whose algorithm the crypto policy rejects (DSA, or RSA shorter than 2048 bits); for a signing subkey, its primary key counts too. Neither a new release signature nor new self-signatures with this key will help. (DSA-1024 can only use 160-bit hashes, which is also why such signatures are SHA-1.)

### What can be done

- Ask upstream to create a new key (for example Ed25519 or RSA 3072+), publish it, and sign releases with it using SHA-256 or better. Then switch the keyring to it.
- Until then the package can keep `%gpgverify`, or verify the tarball differently (for example against a checksum published over HTTPS).

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
