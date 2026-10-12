# Keyring refresh for stunnel

**Status: still-fails**

Failing call: `--keyring=/builddir/new/pgp.asc --signature=/builddir/new/stunnel-5.80.tar.gz.asc --data=/builddir/new/stunnel-5.80.tar.gz`

Phase 1 reason: `sha1-cert`

## pgp.asc

- certificates: AC915EA30645D9D3D4DAE4FEB1048932DD3AAAA3
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 7940 → 13823 bytes

```diff
--- dist-git/pgp.asc
+++ refreshed/pgp.asc
@@ -12,5 +12,6 @@
            UserID: Michał Trojnara <Michal.Trojnara@mirt.net>
            UserID: Michał Trojnara <Michal.Trojnara@mobi-com.net>
            UserID: Michał Trojnara <Michal.Trojnara@stunnel.org>
-self-signatures PositiveCertification: 2022-05-10
+self-signatures PositiveCertification: 2015-02-06, 2022-05-10
 self-signatures SubkeyBinding: 2015-02-06
+third-party GenericCertification: 4
```

## Verification with the refreshed keyring

```
$ sqv ... stunnel-5.80.tar.gz
Signing key on AC915EA30645D9D3D4DAE4FEB1048932DD3AAAA3 is not bound:
           Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

