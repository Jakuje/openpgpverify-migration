Product: Fedora
Component: tor
Version: rawhide
Blocks: 2523619
Summary: tor: source signature does not verify with openpgpverify (several armored blocks in one file)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For tor, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `76e4b6dc9271`):

```
%openpgpverify --keyring=tor-keyring.pub --signature=tor-0.4.9.14.tar.gz.sha256sum.asc --data=tor-0.4.9.14.tar.gz.sha256sum
```

```
Signing key on B74417EDDF22AC9F9E90F49142E86A2A11F48D36 is bad:
           The primary key is not live
  because: Expired on 2023-04-07T12:41:29Z
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

The signature file contains several ASCII-armored blocks concatenated. That is outside the OpenPGP format and Sequoia doesn't read it.

### What can be done

- Keep only the signature by the key in the keyring, or dearmor and join the packets.

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
