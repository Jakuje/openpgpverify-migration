Product: Fedora
Component: dhcp
Version: rawhide
Blocks: 2523619
Summary: dhcp: source signature does not verify with openpgpverify (SHA-1 data signature)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For dhcp, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `ba61518c3ee6`):

```
%openpgpverify --keyring=codesign2021.txt --signature=dhcp-4.4.3-P1.tar.gz.asc --data=dhcp-4.4.3-P1.tar.gz
```

```
Verifying signature:
           Policy rejected non-revocation signature (Binary) requiring collision resistance
  because: SHA1 is not considered secure
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

Checked in full, not only the first error sqv reports: the release signature (v4, SHA-1, made 2022-09-28) is by signing subkey AADBBA5074F1402F7B69D56BC5B4EE931A9F9DFD (RSA 4096 bits) of key 7E1C91AC8030A5A59D1EFAB9750F3C87723E4012 (RSA 4096 bits). The signature itself is rejected: it uses SHA-1. The key itself is fine.

The release signature itself is made with SHA-1. SHA-1 is not accepted for signatures over data because of collision attacks, and this won't be relaxed.

### What can be done

- Ask upstream to sign releases with SHA-256 or better, ideally with a current key.
- Until then the package can keep `%gpgverify`, or verify the tarball differently (for example against a checksum published over HTTPS).

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
