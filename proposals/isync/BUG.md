Product: Fedora
Component: isync
Version: rawhide
Blocks: 2569052
Summary: isync: source signature does not verify with openpgpverify (key expired before signing)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For isync, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `7460df053d65`):

```
%openpgpverify --keyring=isync.keyring --signature=isync-1.5.1.tar.gz.asc --data=isync-1.5.1.tar.gz
```

```
Signing key on 63BFD037CAD71E8DFF3AEA3AC17714F08D1BDBBA is bad:
           The primary key is not live
  because: Expired on 2022-05-22T16:31:18Z
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

The release signature (SHA-512, made 2025-03-11) is by the subkey `106457B8735659A4D40F56456F5447F95D001D85` (RSA 4096 bits) of the key `63BFD037CAD71E8DFF3AEA3AC17714F08D1BDBBA` (RSA 4096 bits). sqv reports only the first problem it hits (above). All the problems found:

- The key expired on 2022-05-22, before the release was signed on 2025-03-11, according to the keyring in dist-git. GnuPG ignores expiry; Sequoia checks that the key was valid when the signature was made.

The copy of the key on keys.openpgp.org, keyserver.ubuntu.com and WKD has the same problems.

### What can be done

- Ask upstream to publish their current key (keys.openpgp.org, WKD or the project website), then update the keyring in dist-git. If the expiry was extended before the release was signed, that is all.
- For the release already in Fedora, ask upstream to sign the same tarball again with the extended key and publish the new signature (the tarball doesn't change), or wait for the next release. Then update the keyring and the signature in dist-git.
- Only if re-signing is not an option: the new self-signatures can be dated one second after the key (or its newest subkey) was created, so that the existing release signatures verify too. Backdating is unusual and easy to get wrong, so it is a last resort; [Updating GPG keys for Fedora and RHEL](https://www.redhat.com/en/blog/updating-gpg-keys-for-fedora-and-rhel) describes how (`gpg --faked-system-time "$((CT + 1))!" --cert-digest-algo SHA256 --quick-set-expire ...`, with `CT` that creation time).

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
