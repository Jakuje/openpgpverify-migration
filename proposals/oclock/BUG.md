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

The release signature (SHA-512, made 2024-12-04) is by the subkey `2F7DBCAD5B30E668BBD516C1CFDF148828C642A7` (RSA 4096 bits) of the key `4A193C06D35E7C670FA4EF0BA2FB9E081F2D130E` (DSA 1024 bits). sqv reports only the first problem it hits (above). All the problems found:

- The primary key is DSA-1024. DSA keys and RSA keys shorter than 2048 bits are no longer considered secure, and the crypto policy rejects them. The release is signed by the subkey, but the primary key that binds the subkey counts too.
- The key expired on 2022-07-21, before the release was signed on 2024-12-04, according to the keyring in dist-git. GnuPG ignores expiry; Sequoia checks that the key was valid when the signature was made.
- The keyring in dist-git has no self-signature for the signing subkey from before 2024-12-04, when the release was signed, so for Sequoia the key wasn't valid yet at that time.

The copy of the key on keys.openpgp.org, keyserver.ubuntu.com and WKD is newer, but its problems remain: key algorithm rejected by the crypto policy.

### What can be done

- Ask upstream to create a new key (for example Ed25519 or RSA 3072+), publish it, and sign releases with it using SHA-256 or better. Then switch the keyring to it.
- Until then the package can keep `%gpgverify`, or verify the tarball differently (for example against a checksum published over HTTPS).

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
