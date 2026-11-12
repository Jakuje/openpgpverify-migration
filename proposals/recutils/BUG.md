Product: Fedora
Component: recutils
Version: rawhide
Blocks: 2569052
Summary: recutils: source signature does not verify with openpgpverify (SHA-1 key self-signatures)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For recutils, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `f8583f348ee8`):

```
%openpgpverify --keyring=gpgkey-BDFA5717FC1DD35C2C3832A23EF90523B304AF08.gpg --signature=recutils-1.9.tar.gz.sig --data=recutils-1.9.tar.gz
```

```
Signing key on BDFA5717FC1DD35C2C3832A23EF90523B304AF08 is not bound:
           No binding signature at time 2022-04-16T17:43:11Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

The release signature (SHA-512, made 2022-04-16) is by the key `BDFA5717FC1DD35C2C3832A23EF90523B304AF08` (RSA 4096 bits). sqv reports only the first problem it hits (above). All the problems found:

- The self-signatures that bind the key's user IDs to it use only SHA-1. SHA-1 is no longer considered secure: collisions have been practical since 2017 (SHAttered) and chosen-prefix collisions since 2020 (SHA-1 is a Shambles), and the crypto policy rejects it. GnuPG doesn't check self-signatures; Sequoia does, and without a valid one it doesn't use the key at all.

The copy of the key on keys.openpgp.org, keyserver.ubuntu.com and WKD has the same problems.

### What can be done

- Ask upstream to refresh the key's self-signatures with SHA-256 and publish the updated key (keys.openpgp.org, WKD or the project website):

      gpg --cert-digest-algo SHA256 --quick-set-expire FPR 2030-12-31
      gpg --cert-digest-algo SHA256 --quick-set-expire FPR 2030-12-31 '*'

  Use an absolute expiry date (or `0`). Releases signed after this verify.
- For the release already in Fedora, ask upstream to sign the same tarball again with the updated key and publish the new signature (the tarball doesn't change), or wait for the next release. Then update the keyring and the signature in dist-git.
- If upstream already signs with a newer key, switch the keyring to that key.
- Only if re-signing is not an option, upstream (only the key owner can do this) can date the new self-signatures one second after the key (or its newest subkey) was created, so that the existing release signatures verify too. Backdating is unusual and easy to get wrong, so it is a last resort; [Updating GPG keys for Fedora and RHEL](https://www.redhat.com/en/blog/updating-gpg-keys-for-fedora-and-rhel) describes how (`gpg --faked-system-time "$((CT + 1))!" --cert-digest-algo SHA256 --quick-set-expire ...`, with `CT` that creation time).
- If upstream doesn't respond, the package can keep `%gpgverify` for now; nothing breaks until it is removed.

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
