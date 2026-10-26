Product: Fedora
Component: skribilo
Version: rawhide
Blocks: 2523619
Summary: skribilo: source signature does not verify with openpgpverify (key expired before signing)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For skribilo, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `1eb78a8eb562`):

```
%openpgpverify --keyring=arunisaac.pub --signature=skribilo-0.11.0.tar.gz.sig --data=skribilo-0.11.0.tar.gz
```

```
Signing key on 7F730343F2F09F3C77BF79D32E25EE8B61802BB3 is bad:
           The primary key is not live
  because: Expired on 2024-03-01T09:44:40Z
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

According to the keyring in dist-git, the signing key had already expired when the release was signed. Usually upstream extended the expiry later and the copy in dist-git is outdated. No newer copy is published on keys.openpgp.org, keyserver.ubuntu.com or WKD. GnuPG ignores expiry; Sequoia checks that the key was valid when the signature was made. (Signatures made while the key was valid keep verifying after it expires.)

### What can be done

- Ask upstream to publish their current key (keys.openpgp.org, WKD or the project website), then update the keyring in dist-git.

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
