Product: Fedora
Component: pdfgrep
Version: rawhide
Blocks: 2523619
Summary: pdfgrep: source signature does not verify with openpgpverify (signing key algorithm rejected)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For pdfgrep, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `968a853d5755`):

```
%openpgpverify --keyring=432FC753112F26D9EB48DDC1A17CF2CA697BEAF2 --signature=pdfgrep-2.2.0.tar.gz.asc --data=pdfgrep-2.2.0.tar.gz
```

```
Signing key on 432FC753112F26D9EB48DDC1A17CF2CA697BEAF2 is not bound:
           Policy rejected asymmetric algorithm
  because: DSA2048 is not considered secure
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

The release signature (SHA-256, made 2024-03-25) is by the subkey `CF01EA7E5A6D59E497266A8434F6B8D85234A348` (DSA 2048 bits) of the key `432FC753112F26D9EB48DDC1A17CF2CA697BEAF2` (RSA 2048 bits). sqv reports only the first problem it hits (above). All the problems found:

- The signing subkey is DSA-2048. DSA keys and RSA keys shorter than 2048 bits are no longer considered secure, and the crypto policy rejects them.

The copy of the key on keys.openpgp.org, keyserver.ubuntu.com and WKD has the same problems.

### What can be done

- Ask upstream to create a new key (for example Ed25519 or RSA 3072+), publish it, and sign releases with it using SHA-256 or better. Then switch the keyring to it.
- Until then the package can keep `%gpgverify`, or verify the tarball differently (for example against a checksum published over HTTPS).

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
