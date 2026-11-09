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

The release signature (SHA-512, made 2023-10-14) is by the key `BAF59BDF98664CEEF14D2A5A6A233DCD47A92289` (RSA 4096 bits). sqv reports only the first problem it hits (above). All the problems found:

- The key expired on 2021-10-08, before the release was signed on 2023-10-14, according to the keyring in dist-git. GnuPG ignores expiry; Sequoia checks that the key was valid when the signature was made.

The copy of the key on keys.openpgp.org, keyserver.ubuntu.com and WKD has the same problems.

### What can be done

- Ask upstream to publish their current key (keys.openpgp.org, WKD or the project website), then update the keyring in dist-git. If the expiry was extended before the release was signed, that is all.
- For the release already in Fedora, ask upstream to sign the same tarball again with the extended key and publish the new signature (the tarball doesn't change), or wait for the next release. Then update the keyring and the signature in dist-git.
- Only if re-signing is not an option: the new self-signatures can be dated one second after the key (or its newest subkey) was created, so that the existing release signatures verify too. Backdating is unusual and easy to get wrong, so it is a last resort; [Updating GPG keys for Fedora and RHEL](https://www.redhat.com/en/blog/updating-gpg-keys-for-fedora-and-rhel) describes how (`gpg --faked-system-time "$((CT + 1))!" --cert-digest-algo SHA256 --quick-set-expire ...`, with `CT` that creation time).

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
