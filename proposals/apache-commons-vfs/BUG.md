Product: Fedora
Component: apache-commons-vfs
Version: rawhide
Blocks: 2523619
Summary: apache-commons-vfs: source signature does not verify with openpgpverify (unreadable v3 key in keyring, SHA-1 self-signatures)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For apache-commons-vfs, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `5d45532e0591`):

```
%openpgpverify --data=commons-vfs-2.9.0-src.tar.gz --signature=commons-vfs-2.9.0-src.tar.gz.asc --keyring=KEYS
```

```
Error: Malformed certificate in keyring "/builddir/new/KEYS"

Caused by:
    Unsupported Cert: Unsupported primary key: Malformed packet: unknown version
openpgpverify: Signature verification failed.
```

### Why

Checked in full, not only the first error sqv reports: the release signature (v4, SHA-512, made 2021-07-17) is by key 2DB4F1EF0FA761ECC4EA935C86FDC7E2A11262CB (RSA 2048 bits). The key in dist-git: the key's self-signatures use only SHA-1. The copy on keyservers/WKD has the same problems.

Two things stand in the way. The keyring contains a version 3 certificate, which Sequoia can't parse; GnuPG skips it silently, but sqv rejects the whole keyring. With the keyring trimmed to the signing key (`gpg --import` into a temporary keyring, then `gpg --export FPR`), sqv reads it, but the signing key's own self-signatures are made with SHA-1, which the Fedora crypto policy rejects. No newer copy of the key with modern self-signatures is published on keys.openpgp.org, keyserver.ubuntu.com or WKD.

### What can be done

- Ask upstream to re-create the key's self-signatures with SHA-256, dated one second after the key was created, and publish the updated key. [Updating GPG keys for Fedora and RHEL](https://www.redhat.com/en/blog/updating-gpg-keys-for-fedora-and-rhel) describes how. The date matters: Sequoia checks how the key was bound when the release was signed, so self-signatures made today (a plain `gpg --quick-set-expire`) only help future releases. With the backdated ones, the existing release signatures verify again. In short (`CT` is the newest creation time from `gpg --list-keys --with-colons --fixed-list-mode FPR`, field 6 of the `pub`/`sub` lines):

      gpg --faked-system-time "$((CT + 1))!" --cert-digest-algo SHA256 --quick-set-expire FPR 2030-12-31
      gpg --faked-system-time "$((CT + 1))!" --cert-digest-algo SHA256 --quick-set-expire FPR 2030-12-31 '*'

  Use an absolute expiry date (or `0`): a relative one such as `4y` counts from the faked time and may already be over. `sqv --keyring KEY.asc RELEASE.sig RELEASE.tar.gz` on an existing release shows whether it worked. Then put a keyring with only the keys that sign releases into dist-git (exported with GnuPG as above, so it has no v3 key).
- If upstream already signs with a newer key, switch the keyring to that key.

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
