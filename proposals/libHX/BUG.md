Product: Fedora
Component: libHX
Version: rawhide
Blocks: 2523619
Summary: libHX: source signature does not verify with openpgpverify (SHA-1 data signature and key self-signatures)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For libHX, the switch can't be done in a simple PR: the current check with `gpgv` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `c99e81fdfdb3`):

```
%openpgpverify --keyring=gpgkey-B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D.gpg --signature=libHX-3.22.tar.asc --data=-
```

```
+ xzcat /builddir/new/libHX-3.22.tar.xz
Signing key on B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D is not bound:
           No binding signature at time 2014-08-25T15:19:26Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

Checked in full, not only the first error sqv reports: the release signature (v4, SHA-1, made 2014-08-25) is by key B56B8B9D9915AA8796EDC013DFFF2CDB19FC338D (RSA 4096 bits). The signature itself is rejected: it uses SHA-1. The key in dist-git: the key's self-signatures use only SHA-1. The copy on keyservers/WKD has the same problems.

Two things use SHA-1, which the Fedora crypto policy rejects. The release signature itself is made with SHA-1; SHA-1 is not accepted for signatures over data because of collision attacks, and this won't be relaxed. The signing key's own self-signatures (user ID certifications or subkey bindings) are SHA-1 too, and that is what sqv reports first above; GnuPG doesn't check them. No newer copy of the key with modern self-signatures is published on keys.openpgp.org, keyserver.ubuntu.com or WKD.

### What can be done

- Ask upstream to do both: refresh the key's self-signatures with SHA-256 and publish the updated key, then sign releases with SHA-256 (`gpg --digest-algo SHA256`, or `personal-digest-preferences SHA256` in `gpg.conf`). A new SHA-256 release signature alone still fails while the key is only bound with SHA-1. Since the old release signatures can't be used anyway, the self-signatures don't need backdating:

      gpg --cert-digest-algo SHA256 --quick-set-expire FPR 2030-12-31
      gpg --cert-digest-algo SHA256 --quick-set-expire FPR 2030-12-31 '*'

  Then update the keyring in dist-git along with the next release.
- If upstream already signs with a newer key, ask them to use SHA-256 with it and switch the keyring to that key.
- Until then the package can keep the current GnuPG check, or verify the tarball differently (for example against a checksum published over HTTPS).

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change replaces the direct GnuPG call with one `%{openpgpverify}` call (same keyring, signature and data) and adds `BuildRequires: openpgpverify`; it is ready and tested up to the signature check. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
