Product: Fedora
Component: libgsasl
Version: rawhide
Blocks: 2523619
Summary: libgsasl: source signature does not verify with openpgpverify (keyring lacks older self-signatures)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For libgsasl, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `957322061f85`):

```
%openpgpverify --keyring=54265e8c.txt --signature=libgsasl-1.10.0.tar.gz.sig --data=libgsasl-1.10.0.tar.gz
```

```
Signing key on 9AA9BDB11BB1B99A21285A330664A76954265E8C is not bound:
           No binding signature at time 2021-01-01T17:01:46Z
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

The keyring in dist-git only has self-signatures that are newer than the release signature, so for Sequoia the key wasn't bound yet when the release was signed. GnuPG doesn't check this. No copy with the older self-signatures is published.

### What can be done

- Export the full key from upstream (with its older self-signatures) and update the keyring in dist-git.

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
