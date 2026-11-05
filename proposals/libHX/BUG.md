Product: Fedora
Component: libHX
Version: rawhide
Blocks: 2523619
Summary: libHX: source signature does not verify with openpgpverify (SHA-1 data signature)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For libHX, the switch can't be done in a simple PR: the current check with `gpgv` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `c99e81fdfdb3`):

```
%openpgpverify --keyring=gpgkey-B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D.gpg --signature=libHX-3.22.tar.asc --data=-
```

```
+ xzcat /builddir/new/libHX-3.22.tar.xz
Signing key on B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D is not bound:
           No binding signature at time 2014-08-25T15:19:26Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

The release signature itself is made with SHA-1 (or with a key algorithm such as DSA-1024 that the policy rejects). SHA-1 is not accepted for signatures over data because of collision attacks, and this won't be relaxed.

### What can be done

- Ask upstream to sign releases with SHA-256 or better, ideally with a current key.
- Until then the package can keep the current GnuPG check, or verify the tarball differently (for example against a checksum published over HTTPS).

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change replaces the direct GnuPG call with one `%{openpgpverify}` call (same keyring, signature and data) and adds `BuildRequires: openpgpverify`; it is ready and tested up to the signature check. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
