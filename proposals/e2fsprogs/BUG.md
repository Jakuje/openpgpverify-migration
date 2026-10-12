Product: Fedora
Component: e2fsprogs
Version: rawhide
Blocks: 2523619
Summary: e2fsprogs: source signature does not verify with openpgpverify (keyring contains a key sqv cannot read)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For e2fsprogs, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `48612ca55f3c`):

```
%openpgpverify --keyring=tytso-key.asc --signature=e2fsprogs-1.47.4.tar.sign --data=-
```

```
Error: Malformed certificate in keyring "/builddir/new/tytso-key.asc"

Caused by:
    Unsupported Cert: Unsupported primary key: Malformed packet: unknown version
openpgpverify: Signature verification failed.
```

### Why

The keyring contains a certificate that Sequoia can't parse (typically an old version 3 key, common in long-lived KEYS files). GnuPG skips such keys silently; sqv rejects the whole keyring, even though the key that signed the release is fine.

### What can be done

- Trim the keyring to the keys that sign releases (for example `gpg --import KEYS` into a temporary keyring, then `gpg --export FPR... > keyring.gpg`), and use that file in the spec.

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
