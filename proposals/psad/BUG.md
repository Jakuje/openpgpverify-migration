Product: Fedora
Component: psad
Version: rawhide
Blocks: 2523619
Summary: psad: source signature does not verify with openpgpverify (signing key algorithm rejected)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For psad, the switch can't be done in a simple PR: the current check with `gpgv2` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `3bc5d8ba3137`):

```
%openpgpverify --keyring=4D6644A9DA036904BDA2CB90E6C9E3350D3E7410.gpg --signature=psad-2.4.6.tar.bz2.asc --data=psad-2.4.6.tar.bz2
```

```
Signing key on 4D6644A9DA036904BDA2CB90E6C9E3350D3E7410 is not bound:
           No binding signature at time 2018-08-01T01:30:39Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

The release signature (SHA-1, made 2018-08-01) is by the key `4D6644A9DA036904BDA2CB90E6C9E3350D3E7410` (DSA 1024 bits). sqv reports only the first problem it hits (above). All the problems found:

- The key is DSA-1024. DSA keys and RSA keys shorter than 2048 bits are no longer considered secure, and the crypto policy rejects them. DSA-1024 can only use 160-bit hashes, which is also why its signatures are SHA-1.
- The self-signatures that bind the key's user IDs to it use only SHA-1. SHA-1 is no longer considered secure: collisions have been practical since 2017 (SHAttered) and chosen-prefix collisions since 2020 (SHA-1 is a Shambles), and the crypto policy rejects it. GnuPG doesn't check self-signatures; Sequoia does, and without a valid one it doesn't use the key at all.
- The release signature itself uses SHA-1 too; for signatures over data, this won't be relaxed.

The copy of the key on keys.openpgp.org, keyserver.ubuntu.com and WKD has the same problems.

### What can be done

- Ask upstream to create a new key (for example Ed25519 or RSA 3072+), publish it, and sign releases with it using SHA-256 or better. Then switch the keyring to it.
- Until then the package can keep the current GnuPG check, or verify the tarball differently (for example against a checksum published over HTTPS).

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change replaces the direct GnuPG call with one `%{openpgpverify}` call (same keyring, signature and data) and adds `BuildRequires: openpgpverify`; it is ready and tested up to the signature check. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
