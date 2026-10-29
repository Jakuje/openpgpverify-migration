Product: Fedora
Component: rnp
Version: rawhide
Blocks: 2523619
Summary: rnp: source signature does not verify with openpgpverify (key expired before signing)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For rnp, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `4606e240df39`):

```
%openpgpverify --keyring=rnp-keyring.gpg --signature=rnp-v0.18.1.tar.gz.asc --data=rnp-v0.18.1.tar.gz
```

```
Signing key on 31AF5A24D861EFCB7CB79A1924900CE0AEFB5417 is bad:
           The subkey is not live
  because: Expired on 2024-09-08T10:52:42Z
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

According to the keyring in dist-git, the signing key had already expired when the release was signed. Usually upstream extended the expiry later and the copy in dist-git is outdated. No newer copy is published on keys.openpgp.org, keyserver.ubuntu.com or WKD. GnuPG ignores expiry; Sequoia checks that the key was valid when the signature was made. (Signatures made while the key was valid keep verifying after it expires.)

### What can be done

- Ask upstream to publish their current key (keys.openpgp.org, WKD or the project website), then update the keyring in dist-git.
- If the expiry was extended only after the release was signed, the new self-signatures have to be dated before the release signature; [Updating GPG keys for Fedora and RHEL](https://www.redhat.com/en/blog/updating-gpg-keys-for-fedora-and-rhel) describes how to backdate them.

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
