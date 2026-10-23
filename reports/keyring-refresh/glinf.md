# Keyring refresh for glinf

**Status: still-fails**

Failing call: `--keyring=/builddir/new/key.txt --signature=/builddir/new/glinf-1.0.tar.gz.sig --data=/builddir/new/glinf-1.0.tar.gz`

Phase 1 reason: `binding-after-signature`

## key.txt

- certificates: 2F61B4828BBA779AECB3F32703A2A4AB1E32FD34
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 1745 → 3569 bytes

```diff
--- dist-git/key.txt
+++ refreshed/key.txt
@@ -3,5 +3,6 @@
            Subkey: B71671110104463D328EECFB31E7BC386BD5DD05
         Key flags: transport encryption, data-at-rest encryption
            UserID: Martin Lambers <marlam@marlam.de>
-self-signatures PositiveCertification: 2020-03-20
-self-signatures SubkeyBinding: 2020-03-20
+self-signatures PositiveCertification: 2017-08-18, 2020-03-20
+self-signatures SubkeyBinding: 2017-08-18, 2020-03-20
+third-party GenericCertification: 2
```

## Verification with the refreshed keyring

```
$ sqv ... glinf-1.0.tar.gz
Signing key on 2F61B4828BBA779AECB3F32703A2A4AB1E32FD34 is bad:
           The primary key is not live
  because: Expired on 2019-08-18T08:38:58Z
rc=1
```

