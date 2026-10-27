# Keyring update from upstream for keepassxc

**Status: proposed**

Failing call: `--keyring=/builddir/new/keepassxc_master_signing_key.asc --signature=/builddir/new/keepassxc-2.8.0-src.tar.xz.sig --data=/builddir/new/keepassxc-2.8.0-src.tar.xz`

Phase 1 reason: `expired`

## keepassxc_master_signing_key.asc

- from: https://keepassxc.org/keepassxc_master_signing_key.asc
- certificates (unchanged): BF5A669F2272CF4324C1FDA8CFB4C2166397D0D2
- size: 50739 → 8009 bytes

```
curl -fsSL -o keepassxc_master_signing_key.asc https://keepassxc.org/keepassxc_master_signing_key.asc
```

```diff
--- dist-git/keepassxc_master_signing_key.asc
+++ upstream/keepassxc_master_signing_key.asc
@@ -1,22 +1,15 @@
       Fingerprint: BF5A669F2272CF4324C1FDA8CFB4C2166397D0D2
         Key flags: certification, signing
            Subkey: 71D4673D73C7F83C17DAE6A2D8538E98A26FD9C4
-                   Invalid: The subkey is not live: Expired on 2024-12-04T12:58:36Z
-  Expiration time: 2024-12-04 12:58:36 UTC (creation time + 7years 11months 4h 16m 27s)
+  Expiration time: 2028-12-08 21:43:56 UTC (creation time + 11years 11months 4days 13h 1m 47s)
         Key flags: signing
            Subkey: AF0AEA44ABAC8F1047733EA7AFF235EEFB5A2517
-                   Revoked:
-                   Invalid: The subkey is not live: Expired on 2021-01-07T18:49:30Z
-  Expiration time: 2021-01-07 18:49:30 UTC (creation time + 4years 4days 6m 18s)
+  Expiration time: 2028-12-08 21:43:56 UTC (creation time + 11years 11months 4days 12h 51m 8s)
         Key flags: signing
            Subkey: C1E4CBA3AD78D3AFD894F9E0B7A66F03B59076A8
-                   Invalid: The subkey is not live: Expired on 2024-12-04T12:59:25Z
-  Expiration time: 2024-12-04 12:59:25 UTC (creation time + 7years 11months 4h 5m 55s)
+  Expiration time: 2028-12-08 21:43:56 UTC (creation time + 11years 11months 4days 12h 50m 26s)
         Key flags: signing
            UserID: KeePassXC Release <release@keepassxc.org>
 self-signatures PositiveCertification: 2017-01-03, 2019-01-08
-self-signatures SubkeyBinding: 2019-01-08, 2020-12-05
+self-signatures SubkeyBinding: 2023-12-10
 self-signatures SubkeyRevocation: 2019-10-25
-third-party CasualCertification: 2
-third-party GenericCertification: 56
-third-party PositiveCertification: 2
```

## Verification with the upstream keyring

```
$ sqv ... keepassxc-2.8.0-src.tar.xz
BF5A669F2272CF4324C1FDA8CFB4C2166397D0D2
rc=0
```

