Product: Fedora
Component: wlroots0.19
Version: rawhide
Blocks: 2523619
Summary: wlroots0.19: source signature does not verify with openpgpverify (key expired before signing)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For wlroots0.19, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `b29d9cc859e8`):

```
%openpgpverify --keyring=gpgkey-0FDE7BE0E88F5E48.gpg --signature=wlroots-0.19.3.tar.gz.sig --data=wlroots-0.19.3.tar.gz
```

```
Signing key on 34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48 is bad:
           The primary key is not live
  because: Expired on 2022-03-10T17:55:59Z
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

According to the keyring in dist-git, the signing key had already expired when the release was signed. Usually upstream extended the expiry later and the copy in dist-git is outdated. No newer copy is published on keys.openpgp.org, keyserver.ubuntu.com or WKD. GnuPG ignores expiry; Sequoia checks that the key was valid when the signature was made. (Signatures made while the key was valid keep verifying after it expires.)

### What can be done

- Ask upstream to publish their current key (keys.openpgp.org, WKD or the project website), then update the keyring in dist-git.

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
