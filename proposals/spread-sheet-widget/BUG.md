Product: Fedora
Component: spread-sheet-widget
Version: rawhide
Blocks: 2523619
Summary: spread-sheet-widget: source signature does not verify with openpgpverify (key expired before signing)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For spread-sheet-widget, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `29dcc4201022`):

```
%openpgpverify --keyring=BAF59BDF98664CEEF14D2A5A6A233DCD47A92289.gpg --signature=spread-sheet-widget-0.10.tar.gz.sig --data=spread-sheet-widget-0.10.tar.gz
```

```
Signing key on BAF59BDF98664CEEF14D2A5A6A233DCD47A92289 is bad:
           The primary key is not live
  because: Expired on 2022-09-08T13:11:47Z
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

According to the keyring in dist-git, the signing key had already expired when the release was signed. Usually upstream extended the expiry later and the copy in dist-git is outdated. No newer copy is published on keys.openpgp.org, keyserver.ubuntu.com or WKD. GnuPG ignores expiry; Sequoia checks that the key was valid when the signature was made. (Signatures made while the key was valid keep verifying after it expires.)

### What can be done

- Ask upstream to publish their current key (keys.openpgp.org, WKD or the project website), then update the keyring in dist-git.

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
