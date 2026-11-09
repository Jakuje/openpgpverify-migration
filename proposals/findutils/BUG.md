Product: Fedora
Component: findutils
Version: rawhide
Blocks: 2523619
Summary: findutils: source signature does not verify with openpgpverify (unreadable v3 key in keyring, SHA-1 self-signatures)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For findutils, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `05405650d77c`):

```
%openpgpverify --keyring=findutils-keyring.gpg --signature=findutils-4.11.0.tar.xz.sig --data=findutils-4.11.0.tar.xz
```

```
Error: Malformed certificate in keyring "/builddir/new/findutils-keyring.gpg"

Caused by:
    Unsupported Cert: Unsupported primary key: Malformed packet: unknown version
openpgpverify: Signature verification failed.
```

### Why

The release signature (SHA-512, made 2026-07-11) is by the key `0CF4E8D871593224842832B888DD9E08C5DDACB9` (RSA 4096 bits). sqv reports only the first problem it hits (above). All the problems found:

- The self-signatures that bind the key's user IDs to it use only SHA-1. SHA-1 is no longer considered secure: collisions have been practical since 2017 (SHAttered) and chosen-prefix collisions since 2020 (SHA-1 is a Shambles), and the crypto policy rejects it. GnuPG doesn't check self-signatures; Sequoia does, and without a valid one it doesn't use the key at all.
- The keyring also contains a version 3 key, which Sequoia can't parse. GnuPG skips it silently; sqv rejects the whole keyring.

The copy of the key on keys.openpgp.org, keyserver.ubuntu.com and WKD has the same problems.

### What can be done

- Ask upstream to refresh the key's self-signatures with SHA-256 and publish the updated key (keys.openpgp.org, WKD or the project website):

      gpg --cert-digest-algo SHA256 --quick-set-expire FPR 2030-12-31
      gpg --cert-digest-algo SHA256 --quick-set-expire FPR 2030-12-31 '*'

  Use an absolute expiry date (or `0`). Releases signed after this verify.
- Use a keyring with only the keys that sign releases (`gpg --import KEYS` into a temporary keyring, then `gpg --export FPR... > keyring.gpg`), so it has no v3 key.
- For the release already in Fedora, ask upstream to sign the same tarball again with the updated key and publish the new signature (the tarball doesn't change), or wait for the next release. Then update the keyring and the signature in dist-git.
- Only if re-signing is not an option: the new self-signatures can be dated one second after the key (or its newest subkey) was created, so that the existing release signatures verify too. Backdating is unusual and easy to get wrong, so it is a last resort; [Updating GPG keys for Fedora and RHEL](https://www.redhat.com/en/blog/updating-gpg-keys-for-fedora-and-rhel) describes how (`gpg --faked-system-time "$((CT + 1))!" --cert-digest-algo SHA256 --quick-set-expire ...`, with `CT` that creation time).

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
