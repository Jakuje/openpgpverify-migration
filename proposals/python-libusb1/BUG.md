Product: Fedora
Component: python-libusb1
Version: rawhide
Blocks: 2523619
Summary: python-libusb1: source signature does not verify with openpgpverify (SHA-1 key self-signatures)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For python-libusb1, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `7fadad9c399b`):

```
%openpgpverify --keyring=gpgkey-python-libusb1.gpg --signature=libusb1-3.4.0.tar.gz.asc --data=libusb1-3.4.0.tar.gz
```

```
Signing key on 983AE8B73B9115987A923845CAC936914257B0C1 is not bound:
           No binding signature at time 2026-05-16T20:57:41Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

The signing key's own self-signatures (user ID certifications or subkey bindings) are made with SHA-1. The Fedora crypto policy rejects SHA-1, and Sequoia applies the policy to key bindings too; GnuPG doesn't check them. No newer copy of the key with modern self-signatures is published on keys.openpgp.org, keyserver.ubuntu.com or WKD.

### What can be done

- Ask upstream to re-create the key's self-signatures with SHA-256, dated one second after the key was created, and publish the updated key. [Updating GPG keys for Fedora and RHEL](https://www.redhat.com/en/blog/updating-gpg-keys-for-fedora-and-rhel) describes how. The date matters: Sequoia checks how the key was bound when the release was signed, so self-signatures made today (a plain `gpg --quick-set-expire`) only help future releases. With the backdated ones, the existing release signatures verify again. In short (`CT` is the newest creation time from `gpg --list-keys --with-colons --fixed-list-mode FPR`, field 6 of the `pub`/`sub` lines):

      gpg --faked-system-time "$((CT + 1))!" --cert-digest-algo SHA256 --quick-set-expire FPR 2030-12-31
      gpg --faked-system-time "$((CT + 1))!" --cert-digest-algo SHA256 --quick-set-expire FPR 2030-12-31 '*'

  Use an absolute expiry date (or `0`): a relative one such as `4y` counts from the faked time and may already be over. `sqv --keyring KEY.asc RELEASE.sig RELEASE.tar.gz` on an existing release shows whether it worked. Then refresh the keyring in dist-git.
- If upstream already signs with a newer key, switch the keyring to that key.

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
