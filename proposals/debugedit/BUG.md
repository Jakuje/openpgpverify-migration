Product: Fedora
Component: debugedit
Version: rawhide
Blocks: 2523619
Summary: debugedit: source signature does not verify with openpgpverify (GnuPG keybox keyring)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For debugedit, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `05b2db3e94a3`):

```
%openpgpverify --keyring=gpgkey-CBA20376A15C6FFC11CD.gpg --signature=debugedit-5.3.tar.xz.sig --data=debugedit-5.3.tar.xz
```

```
Error: Failed to parse keyring "/builddir/new/gpgkey-CBA20376A15C6FFC11CD.gpg"

Caused by:
    File appears to be in keybox format, which is not supported
openpgpverify: Signature verification failed.
```

### Why

The keyring file is in GnuPG's keybox format, which only GnuPG can read.

### What can be done

- Convert it to an OpenPGP keyring: `gpg --no-default-keyring --keyring ./FILE --export > FILE.gpg`, and use that file.

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
