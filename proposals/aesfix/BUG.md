Product: Fedora
Component: aesfix
Version: rawhide
Blocks: 2523619
Summary: aesfix: source signature does not verify with openpgpverify (signing key algorithm rejected)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For aesfix, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `0640c1ac57d2`):

```
%openpgpverify --keyring=gpgkey-12E404FFD3C931F934052D06B8841A919D0FACE4.gpg --signature=aesfix-1.0.1.tar.gz.asc --data=aesfix-1.0.1.tar.gz
```

```
Error: Policy rejected packet type

Caused by:
    Signature Packet v3 is not considered secure since 2021-02-01T00:00:00Z
openpgpverify: Signature verification failed.
```

### Why

The release signature (SHA-1, made 2008-07-18) is by the key `12E404FFD3C931F934052D06B8841A919D0FACE4` (DSA 1024 bits). sqv reports only the first problem it hits (above). All the problems found:

- The key is DSA-1024. DSA keys and RSA keys shorter than 2048 bits are no longer considered secure, and the crypto policy rejects them. DSA-1024 can only use 160-bit hashes, which is also why its signatures are SHA-1.
- The keyring in dist-git has no self-signature from before 2008-07-18, when the release was signed, so for Sequoia the key wasn't valid yet at that time.
- The release signature is in the version 3 (PGP 2) format, which current OpenPGP implementations no longer accept.
- The release signature itself uses SHA-1. SHA-1 is no longer considered secure: collisions have been practical since 2017 (SHAttered) and chosen-prefix collisions since 2020 (SHA-1 is a Shambles), and the crypto policy rejects it; for signatures over data, this won't be relaxed.

The copy of the key on keys.openpgp.org, keyserver.ubuntu.com and WKD is newer, but its problems remain: key algorithm rejected by the crypto policy, the key's self-signatures use only SHA-1.

### What can be done

- Ask upstream to create a new key (for example Ed25519 or RSA 3072+), publish it, and sign releases with it using SHA-256 or better. Then switch the keyring to it.
- Until then the package can keep `%gpgverify`, or verify the tarball differently (for example against a checksum published over HTTPS).

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
