Product: Fedora
Component: xforms
Version: rawhide
Blocks: 2523619
Summary: xforms: source signature does not verify with openpgpverify (SHA-1 data signature)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For xforms, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `221aeb9d604e`):

```
%openpgpverify --keyring=gpgkey-B5049F22184B56AF7C3AFBDBEB9474E50D5C15EB.gpg --signature=xforms-1.2.4.tar.gz.sig --data=xforms-1.2.4.tar.gz
```

```
Signing key on B5049F22184B56AF7C3AFBDBEB9474E50D5C15EB is not bound:
           No binding signature at time 2014-06-28T20:46:55Z
  because: No binding signature at time 2014-06-28T20:46:55Z
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

The release signature itself is made with SHA-1 (or with a key algorithm such as DSA-1024 that the policy rejects). SHA-1 is not accepted for signatures over data because of collision attacks, and this won't be relaxed.

### What can be done

- Ask upstream to sign releases with SHA-256 or better, ideally with a current key.
- Until then the package can keep `%gpgverify`, or verify the tarball differently (for example against a checksum published over HTTPS).

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
