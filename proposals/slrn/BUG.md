Product: Fedora
Component: slrn
Version: rawhide
Blocks: 2523619
Summary: slrn: source signature does not verify with openpgpverify (OpenPGP v3 signature)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For slrn, the switch can't be done in a simple PR: the current check with `gpgv2` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `80300b0556c6`):

```
%openpgpverify --keyring=slrn-gpgkeys.gpg --signature=slrn-1.0.3a.tar.bz2.asc --data=slrn-1.0.3a.tar.bz2
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
- Otherwise, consider verifying against a checksum, or keep the current GnuPG check for now.

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change replaces the direct GnuPG call with one `%{openpgpverify}` call (same keyring, signature and data) and adds `BuildRequires: openpgpverify`; it is ready and tested up to the signature check. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
