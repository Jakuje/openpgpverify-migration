Product: Fedora
Component: libisoburn
Version: rawhide
Blocks: 2569052
Summary: libisoburn: source signature does not verify with openpgpverify (signing key algorithm rejected)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For libisoburn, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `74c3acfc8d25`):

```
%openpgpverify --keyring=44BC9FD0D688EB007C4DD029E9CBDFC0ABC0A854 --signature=libisoburn-1.5.8.pl02.tar.gz.sig --data=libisoburn-1.5.8.pl02.tar.gz
```

```
Signing key on 44BC9FD0D688EB007C4DD029E9CBDFC0ABC0A854 is not bound:
           No binding signature at time 2026-05-22T16:41:00Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

The release signature (SHA-1, made 2026-05-22) is by the key `44BC9FD0D688EB007C4DD029E9CBDFC0ABC0A854` (DSA 1024 bits). sqv reports only the first problem it hits (above). All the problems found:

- The key is DSA-1024. DSA keys and RSA keys shorter than 2048 bits are no longer considered secure, and the crypto policy rejects them. DSA-1024 can only use 160-bit hashes, which is also why its signatures are SHA-1.
- The self-signatures that bind the key's user IDs to it use only SHA-1. SHA-1 is no longer considered secure: collisions have been practical since 2017 (SHAttered) and chosen-prefix collisions since 2020 (SHA-1 is a Shambles), and the crypto policy rejects it. GnuPG doesn't check self-signatures; Sequoia does, and without a valid one it doesn't use the key at all.
- The release signature itself uses SHA-1 too; for signatures over data, this won't be relaxed.

The copy of the key on keys.openpgp.org, keyserver.ubuntu.com and WKD has the same problems.

### What can be done

- Ask upstream to create a new key (for example Ed25519 or RSA 3072+), publish it, and sign releases with it using SHA-256 or better. Then switch the keyring to it.
- Until then the package can keep `%gpgverify`, or verify the tarball differently (for example against a checksum published over HTTPS).

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
