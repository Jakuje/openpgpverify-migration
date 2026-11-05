# Keyring update from upstream for mingw-nettle

**Status: proposed**

Failing call: `--keyring=/builddir/new/nettle-release-keyring.gpg --signature=/builddir/new/nettle-3.10.2.tar.gz.sig --data=/builddir/new/nettle-3.10.2.tar.gz`

Phase 1 reason: `expired`

## nettle-release-keyring.gpg

- from: https://keys.openpgp.org/vks/v1/by-fingerprint/343C2FF0FBEE5EC2EDBEF399F3599FF828C67298#/nettle-release-keyring.asc
- **renamed to `nettle-release-keyring.asc`; its `Source` line becomes the URL**
- certificates (unchanged): 343C2FF0FBEE5EC2EDBEF399F3599FF828C67298
- size: 31405 → 5662 bytes

```
curl -fsSL -o nettle-release-keyring.asc 'https://keys.openpgp.org/vks/v1/by-fingerprint/343C2FF0FBEE5EC2EDBEF399F3599FF828C67298'
```

```diff
--- dist-git/nettle-release-keyring.gpg
+++ upstream/nettle-release-keyring.gpg
@@ -1,16 +1,10 @@
       Fingerprint: 343C2FF0FBEE5EC2EDBEF399F3599FF828C67298
-                   Invalid: The primary key is not live: Expired on 2025-01-15T17:12:43Z
-  Expiration time: 2025-01-15 17:12:43 UTC (creation time + 12years 7days 21h 46m 16s)
+  Expiration time: 2030-06-25 18:39:13 UTC (creation time + 17years 5months 16days 12h 24m 46s)
         Key flags: certification, signing
            Subkey: 48C9DE74746361F8617018347520153007F35B23
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-01-15T17:12:43Z
-  Expiration time: 2025-01-15 17:21:19 UTC (creation time + 12years 7days 21h 54m 52s)
+  Expiration time: 2030-06-25 18:40:52 UTC (creation time + 17years 5months 16days 12h 26m 25s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Niels Möller <nisse@lysator.liu.se>
-self-signatures PositiveCertification: 2013-01-07, 2020-01-17
-self-signatures SubkeyBinding: 2013-01-07, 2020-01-17
-third-party CasualCertification: 7
+self-signatures PositiveCertification: 2013-01-07, 2020-01-17, 2025-06-26
+self-signatures SubkeyBinding: 2013-01-07, 2020-01-17, 2025-06-26
 third-party CertificationRevocation: 1
-third-party GenericCertification: 16
-third-party PersonaCertification: 1
-third-party PositiveCertification: 3
```

## Verification with the upstream keyring

```
$ sqv ... nettle-3.10.2.tar.gz
343C2FF0FBEE5EC2EDBEF399F3599FF828C67298
rc=0
```

