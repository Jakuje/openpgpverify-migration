Product: Fedora
Component: glinf
Version: rawhide
Blocks: 2523619
Summary: glinf: source signature does not verify with openpgpverify (keyring lacks older self-signatures)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For glinf, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `1356a8b52e4a`):

```
%openpgpverify --keyring=key.txt --signature=glinf-1.0.tar.gz.sig --data=glinf-1.0.tar.gz
```

```
Signing key on 2F61B4828BBA779AECB3F32703A2A4AB1E32FD34 is not bound:
           No binding signature at time 2020-01-29T09:03:14Z
  because: No binding signature at time 2020-01-29T09:03:14Z
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

The release signature (SHA-512, made 2020-01-29) is by the key `2F61B4828BBA779AECB3F32703A2A4AB1E32FD34` (RSA 2048 bits). sqv reports only the first problem it hits (above). All the problems found:

- The keyring in dist-git has no self-signature from before 2020-01-29, when the release was signed, so for Sequoia the key wasn't valid yet at that time.

The copy of the key on keys.openpgp.org, keyserver.ubuntu.com and WKD is newer, but its problems remain: the key had expired when the release was signed.

### What can be done

- Export the full key from upstream (with its older self-signatures) and update the keyring in dist-git.

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
