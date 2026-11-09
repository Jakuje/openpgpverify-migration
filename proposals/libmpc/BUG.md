Product: Fedora
Component: libmpc
Version: rawhide
Blocks: 2569052
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

The release signature (SHA-256, made 2026-04-16) is by the key `AD17A21EF8AED8F1CC02DBD9F7D5C9BF765C61E3` (DSA 2048 bits). sqv reports only the first problem it hits (above). All the problems found:

- The key is DSA-2048. DSA keys and RSA keys shorter than 2048 bits are no longer considered secure, and the crypto policy rejects them.
- The key expired on 2024-06-03, before the release was signed on 2026-04-16, according to the keyring in dist-git. GnuPG ignores expiry; Sequoia checks that the key was valid when the signature was made.

The copy of the key on keys.openpgp.org, keyserver.ubuntu.com and WKD is newer, but its problems remain: key algorithm rejected by the crypto policy.

### What can be done

- Ask upstream to create a new key (for example Ed25519 or RSA 3072+), publish it, and sign releases with it using SHA-256 or better. Then switch the keyring to it.
- Until then the package can keep `%gpgverify`, or verify the tarball differently (for example against a checksum published over HTTPS).

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
