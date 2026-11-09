Product: Fedora
Component: ed
Version: rawhide
Blocks: 2569052
Summary: ed: source signature does not verify with openpgpverify (SHA-1 data signature and key self-signatures)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For ed, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `6722a7d94a64`):

```
%openpgpverify --keyring=antoniodiazdiaz-keyring-2026.asc --signature=ed-1.22.6.tar.lz.sig --data=ed-1.22.6.tar.lz
```

```
Signing key on 1E5AEE0B18C0DEB45D64AA0325B62C9821501AA0 is not bound:
           No binding signature at time 2026-08-20T15:50:42Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

The release signature (SHA-1, made 2026-08-20) is by the key `1E5AEE0B18C0DEB45D64AA0325B62C9821501AA0` (RSA 4096 bits). sqv reports only the first problem it hits (above). All the problems found:

- The self-signatures that bind the key's user IDs to it use only SHA-1. SHA-1 is no longer considered secure: collisions have been practical since 2017 (SHAttered) and chosen-prefix collisions since 2020 (SHA-1 is a Shambles), and the crypto policy rejects it. GnuPG doesn't check self-signatures; Sequoia does, and without a valid one it doesn't use the key at all.
- The release signature itself uses SHA-1 too; for signatures over data, this won't be relaxed.

The copy of the key on keys.openpgp.org, keyserver.ubuntu.com and WKD has the same problems.

### What can be done

- Ask upstream to refresh the key's self-signatures with SHA-256 and publish the updated key (keys.openpgp.org, WKD or the project website):

      gpg --cert-digest-algo SHA256 --quick-set-expire FPR 2030-12-31
      gpg --cert-digest-algo SHA256 --quick-set-expire FPR 2030-12-31 '*'

  Use an absolute expiry date (or `0`). A new SHA-256 release signature alone still fails while the key is only bound with SHA-1.
- Then ask upstream to sign releases with SHA-256 (`gpg --digest-algo SHA256`, or `personal-digest-preferences SHA256` in `gpg.conf`): the current release again, or the next one. Then update the keyring and the signature in dist-git.
- If upstream already signs with a newer key, ask them to use SHA-256 with it and switch the keyring to that key.
- Until then the package can keep `%gpgverify`, or verify the tarball differently (for example against a checksum published over HTTPS).

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
