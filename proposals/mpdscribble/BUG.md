Product: Fedora
Component: mpdscribble
Version: rawhide
Blocks: 2523619
Summary: mpdscribble: source signature does not verify with openpgpverify (SHA-1 key self-signatures)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). For mpdscribble, the switch can't be done in a simple PR: `%gpgverify` accepts the current upstream signature, but `%openpgpverify` rejects it.

Failing check (dist-git commit `6d0aa38065ea`):

```
%openpgpverify --keyring=0392335A78083894A4301C43236E8A58C6DB4512.gpg --signature=mpdscribble-0.25.tar.xz.sig --data=mpdscribble-0.25.tar.xz
```

```
Signing key on 0392335A78083894A4301C43236E8A58C6DB4512 is not bound:
           No binding signature at time 2023-12-11T17:22:41Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

The signing key's own self-signatures (user ID certifications or subkey bindings) are made with SHA-1. The Fedora crypto policy rejects SHA-1, and Sequoia applies the policy to key bindings too; GnuPG doesn't check them. No newer copy of the key with modern self-signatures is published on keys.openpgp.org, keyserver.ubuntu.com or WKD.

### What can be done

- Ask upstream to re-create the key's self-signatures with a modern hash and publish the updated key; renewing the expiry does that (`gpg --cert-digest-algo SHA512 --quick-set-expire FPR 2y`, and again with `'*'` for the subkeys). Then refresh the keyring in dist-git.
- If upstream already signs with a newer key, switch the keyring to that key.

The rest of the conversion is mechanical. Once the signature or key is sorted out, the spec change is the same as for other packages: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. I'm happy to send the PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
