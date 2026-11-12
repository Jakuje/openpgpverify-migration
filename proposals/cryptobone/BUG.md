Product: Fedora
Component: cryptobone
Version: rawhide
Blocks: 2569052
Summary: cryptobone: source signature does not verify with openpgpverify (SHA-1 key self-signatures)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For cryptobone, the switch can't be done in a simple PR: the current check with `gpg2` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `416099131063`):

```
%openpgpverify --keyring=gpgkey-3274CB29956498038A9C874BFBF6E2C28E9C98DD.asc --signature=cryptobone-2.2.tar.gz.asc --data=cryptobone-2.2.tar.gz
```

```
Signing key on 3274CB29956498038A9C874BFBF6E2C28E9C98DD is not bound:
           No binding signature at time 2026-08-20T05:55:23Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

The release signature (SHA-512, made 2026-08-20) is by the key `3274CB29956498038A9C874BFBF6E2C28E9C98DD` (RSA 4096 bits). sqv reports only the first problem it hits (above). All the problems found:

- The self-signatures that bind the key's user IDs to it use only SHA-1. SHA-1 is no longer considered secure: collisions have been practical since 2017 (SHAttered) and chosen-prefix collisions since 2020 (SHA-1 is a Shambles), and the crypto policy rejects it. GnuPG doesn't check self-signatures; Sequoia does, and without a valid one it doesn't use the key at all.

The key is not published on keys.openpgp.org, keyserver.ubuntu.com and WKD.

### What can be done

- Ask upstream to refresh the key's self-signatures with SHA-256 and publish the updated key (keys.openpgp.org, WKD or the project website):

      gpg --cert-digest-algo SHA256 --quick-set-expire FPR 2030-12-31
      gpg --cert-digest-algo SHA256 --quick-set-expire FPR 2030-12-31 '*'

  Use an absolute expiry date (or `0`). Releases signed after this verify.
- For the release already in Fedora, ask upstream to sign the same tarball again with the updated key and publish the new signature (the tarball doesn't change), or wait for the next release. Then update the keyring and the signature in dist-git.
- If upstream already signs with a newer key, switch the keyring to that key.
- Only if re-signing is not an option, upstream (only the key owner can do this) can date the new self-signatures one second after the key (or its newest subkey) was created, so that the existing release signatures verify too. Backdating is unusual and easy to get wrong, so it is a last resort; [Updating GPG keys for Fedora and RHEL](https://www.redhat.com/en/blog/updating-gpg-keys-for-fedora-and-rhel) describes how (`gpg --faked-system-time "$((CT + 1))!" --cert-digest-algo SHA256 --quick-set-expire ...`, with `CT` that creation time).
- If upstream doesn't respond, the package can keep the current GnuPG check for now; nothing breaks until it is removed.

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change replaces the direct GnuPG call with one `%{openpgpverify}` call (same keyring, signature and data) and adds `BuildRequires: openpgpverify`; it is ready and tested up to the signature check. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
