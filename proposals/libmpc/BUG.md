Product: Fedora
Component: libmpc
Version: rawhide
Blocks: 2523619
Summary: libmpc: source signature does not verify with openpgpverify (signing key algorithm rejected)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For libmpc, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `41e31fd571b6`):

```
%openpgpverify --data=mpc-1.4.1.tar.xz --signature=mpc-1.4.1.tar.xz.sig --keyring=enge.gpg
```

```
Signing key on AD17A21EF8AED8F1CC02DBD9F7D5C9BF765C61E3 is not bound:
           Policy rejected asymmetric algorithm
  because: DSA2048 is not considered secure
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

The release is signed with a key whose algorithm the crypto policy rejects (DSA, or RSA shorter than 2048 bits). A new signature with the same key won't help.

### What can be done

- Ask upstream to sign releases with a current key (for example Ed25519 or RSA 3072+), then switch the keyring to it.
- Until then the package can keep `%gpgverify`.

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
