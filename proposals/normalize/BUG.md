Product: Fedora
Component: normalize
Version: rawhide
Blocks: 2523619
Summary: normalize: source signature does not verify with openpgpverify (OpenPGP v3 signature)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For normalize, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `2575c100d9e2`):

```
%openpgpverify --keyring=0xAFC8519A83FE7486.gpg --signature=normalize-0.7.7.tar.gz.sig --data=normalize-0.7.7.tar.gz
```

```
Error: Policy rejected packet type

Caused by:
    Signature Packet v3 is not considered secure since 2021-02-01T00:00:00Z
openpgpverify: Signature verification failed.
```

### Why

The release signature uses the version 3 signature format, which OpenPGP implementations have rejected since 2021.

### What can be done

- Ask upstream to re-sign the release with a current key, if upstream is still active.
- Otherwise, consider verifying against a checksum, or keep `%gpgverify` for now.

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
