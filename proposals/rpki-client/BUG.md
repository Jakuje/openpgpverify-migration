Product: Fedora
Component: rpki-client
Version: rawhide
Blocks: 2523619
Summary: rpki-client: source signature does not verify with openpgpverify (key expired before signing)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For rpki-client, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `361aac0b05d3`):

```
%openpgpverify --keyring=B5B6416FEA6DDA05EA562A9FCB987F2783972FF9 --signature=rpki-client-9.9.tar.gz.asc --data=rpki-client-9.9.tar.gz
```

```
Signing key on B5B6416FEA6DDA05EA562A9FCB987F2783972FF9 is bad:
           The primary key is not live
  because: Expired on 2026-03-18T18:43:06Z
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

According to the keyring in dist-git, the signing key had already expired when the release was signed. Usually upstream extended the expiry later and the copy in dist-git is outdated. No newer copy is published on keys.openpgp.org, keyserver.ubuntu.com or WKD. GnuPG ignores expiry; Sequoia checks that the key was valid when the signature was made. (Signatures made while the key was valid keep verifying after it expires.)

### What can be done

- Ask upstream to publish their current key (keys.openpgp.org, WKD or the project website), then update the keyring in dist-git.

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
