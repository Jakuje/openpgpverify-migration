Product: Fedora
Component: xcb-util-errors
Version: rawhide
Blocks: 2523619
Summary: xcb-util-errors: source signature does not verify with openpgpverify (keyring lacks older self-signatures)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For xcb-util-errors, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `0fd4b58b5c0b`):

```
%openpgpverify --keyring=gpgkey-A2FB9E081F2D130E.gpg --signature=xcb-util-errors-1.0.1.tar.xz.sig --data=xcb-util-errors-1.0.1.tar.xz
```

```
Signing key on 4A193C06D35E7C670FA4EF0BA2FB9E081F2D130E is not bound:
           primary key
  because: No binding signature at time 2022-10-19T01:14:15Z
  because: No binding signature at time 2022-10-19T01:14:15Z
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

The keyring in dist-git only has self-signatures that are newer than the release signature, so for Sequoia the key wasn't bound yet when the release was signed. GnuPG doesn't check this. No copy with the older self-signatures is published.

### What can be done

- Export the full key from upstream (with its older self-signatures) and update the keyring in dist-git.

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
