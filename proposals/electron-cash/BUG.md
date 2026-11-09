Product: Fedora
Component: electron-cash
Version: rawhide
Blocks: 2523619
Summary: electron-cash: source signature does not verify with openpgpverify (signing key algorithm rejected)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For electron-cash, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `ba7382ee9bfb`):

```
%openpgpverify --keyring=gpgkey-electron-cash.gpg --signature=electron_cash-4.4.6.tar.gz.asc --data=electron_cash-4.4.6.tar.gz
```

```
Signing key on D56C110F4555F371AEEFCB254FD06489EFF1DDE1 is not bound:
           Policy rejected asymmetric algorithm
  because: DSA2048 is not considered secure
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

Checked in full, not only the first error sqv reports: the release signature (v4, SHA-256, made 2026-08-11) is by key D56C110F4555F371AEEFCB254FD06489EFF1DDE1 (DSA 2048 bits). The key in dist-git: key algorithm rejected by the crypto policy (DSA-2048). The copy on keyservers/WKD has the same problems.

The release is signed with a key whose algorithm the crypto policy rejects (DSA, or RSA shorter than 2048 bits); for a signing subkey, its primary key counts too. Neither a new release signature nor new self-signatures with this key will help. (DSA-1024 can only use 160-bit hashes, which is also why such signatures are SHA-1.)

### What can be done

- Ask upstream to create a new key (for example Ed25519 or RSA 3072+), publish it, and sign releases with it using SHA-256 or better. Then switch the keyring to it.
- Until then the package can keep `%gpgverify`, or verify the tarball differently (for example against a checksum published over HTTPS).

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
