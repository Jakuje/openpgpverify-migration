Product: Fedora
Component: cgit
Version: rawhide
Blocks: 2569052
Summary: cgit: source signature does not verify with openpgpverify (git key with SHA-1 self-signatures)

---

As part of the Fedora 45 Change [Sequoia openpgpverify](https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify), `%gpgverify` (GnuPG) is being replaced by `%openpgpverify` (Sequoia `sqv`). cgit verifies two tarballs: its own and the bundled git. Its own check can be switched after a keyring refresh, but `%openpgpverify` rejects the signature of the git tarball, while `%gpgverify` accepts it.

Failing check (dist-git commit `72263f147e2a`, cgit 1.3 with git 2.53.0):

```
xz -dc '%{SOURCE1}' | %{openpgpverify} --keyring='%{SOURCE91}' --signature='%{SOURCE93}' --data=-
```

```
Signing key on 96E07AF25771955980DAD10020D04E5A713660A7 is not bound:
           primary key
  because: No binding signature at time 2026-02-02T02:38:56Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
0 of 1 signatures are valid (threshold is: 1).
openpgpverify: Signature verification failed.
```

### Why

The git tarball is signed (SHA-256) by Junio C Hamano's subkey `E1F036B1FEE7221FC778ECEFB0B5E88696AFE6CB` of the key `96E07AF25771955980DAD10020D04E5A713660A7`. The self-signatures that bind the key's user IDs and subkeys to it use only SHA-1, which the crypto policy rejects; GnuPG doesn't check self-signatures, Sequoia does, and without a valid one it doesn't use the key at all. The copies on keys.openpgp.org, keyserver.ubuntu.com and WKD have the same problem. This is the same key and the same problem as in the git package: [rhbz#2569328](https://bugzilla.redhat.com/show_bug.cgi?id=2569328).

cgit's own key (`AB9942E6D4A4CFC3412620A749FC7012A5DE03AE`) is fine once refreshed: the copy in dist-git expired in 2022, and the copy at the URL in the spec (https://www.zx2c4.com/keys/AB9942E6D4A4CFC3412620A749FC7012A5DE03AE.asc) has a renewed expiry and verifies cgit 1.3.

### What can be done

- The git key needs an upstream fix: refreshed self-signatures with SHA-256, published by Junio. That is tracked in rhbz#2569328; once git can switch, cgit can take the same `gpgkey-96E07AF25771955980DAD10020D04E5A713660A7.asc`.
- cgit's own key can be refreshed now, byte for byte from the URL in the spec:

      curl -fsSL -o gpgkey-AB9942E6D4A4CFC3412620A749FC7012A5DE03AE.asc https://www.zx2c4.com/keys/AB9942E6D4A4CFC3412620A749FC7012A5DE03AE.asc

The rest of the conversion is mechanical: `%{gpgverify}` → `%{openpgpverify}` and `BuildRequires: openpgpverify`. The keyring refresh and the conversion are prepared as two commits in [proposals/cgit](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/cgit); the refresh can go in now, the conversion once the git key is fixed. I'm happy to send either as a PR.

(The check was run with scripts from https://github.com/Jakuje/openpgpverify-migration.)
