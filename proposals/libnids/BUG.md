Product: Fedora
Component: libnids
Version: rawhide
Blocks: 2523619
Summary: libnids: source signature does not verify with openpgpverify (SHA-1 data signature)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For libnids, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `54fae1462020`):

```
%openpgpverify --keyring=gpgkey-67E00C8AE6DEE3486468F6C6E20D29536F5C037F.gpg --signature=libnids-1.24.tar.gz.asc --data=libnids-1.24.tar.gz
```

```
Signing key on 67E00C8AE6DEE3486468F6C6E20D29536F5C037F is not bound:
           No binding signature at time 2010-03-14T10:52:10Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
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
