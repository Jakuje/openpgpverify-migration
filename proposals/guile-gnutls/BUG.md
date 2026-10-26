Product: Fedora
Component: guile-gnutls
Version: rawhide
Blocks: 2523619
Summary: guile-gnutls: source signature does not verify with openpgpverify (key expired before signing)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For guile-gnutls, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `91dba79547ee`):

```
%openpgpverify --keyring=gnu-keyring.gpg --signature=guile-gnutls-3.7.14.tar.gz.sig --data=guile-gnutls-3.7.14.tar.gz
```

```
Signing key on B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE is bad:
           The primary key is not live
  because: Expired on 2022-05-17T06:38:35Z
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

According to the keyring in dist-git, the signing key had already expired when the release was signed. Usually upstream extended the expiry later and the copy in dist-git is outdated. No newer copy is published on keys.openpgp.org, keyserver.ubuntu.com or WKD. GnuPG ignores expiry; Sequoia checks that the key was valid when the signature was made. (Signatures made while the key was valid keep verifying after it expires.)

### What can be done

- Ask upstream to publish their current key (keys.openpgp.org, WKD or the project website), then update the keyring in dist-git.

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
