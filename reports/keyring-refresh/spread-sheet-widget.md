# Keyring refresh for spread-sheet-widget

**Status: still-fails**

Failing call: `--keyring=/builddir/new/BAF59BDF98664CEEF14D2A5A6A233DCD47A92289.gpg --signature=/builddir/new/spread-sheet-widget-0.10.tar.gz.sig --data=/builddir/new/spread-sheet-widget-0.10.tar.gz`

Phase 1 reason: `expired`

## BAF59BDF98664CEEF14D2A5A6A233DCD47A92289.gpg

- certificates: BAF59BDF98664CEEF14D2A5A6A233DCD47A92289
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 2261 → 2902 bytes

```diff
--- dist-git/BAF59BDF98664CEEF14D2A5A6A233DCD47A92289.gpg
+++ refreshed/BAF59BDF98664CEEF14D2A5A6A233DCD47A92289.gpg
@@ -4,8 +4,8 @@
         Key flags: certification, signing
            Subkey: 43F2EA798EF568E7FB234BBAA0C9E80D28FB7BD0
                    Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-09-08T13:11:47Z
-  Expiration time: 2022-09-08 13:11:47 UTC (creation time + 4years 11months 29days 3h 50m 24s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: John Darrington <jmd@gnu.org>
 self-signatures PositiveCertification: 2017-09-09
-self-signatures SubkeyBinding: 2017-09-09
+self-signatures SubkeyBinding: 2017-09-09, 2023-10-01
+third-party GenericCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... spread-sheet-widget-0.10.tar.gz
Signing key on BAF59BDF98664CEEF14D2A5A6A233DCD47A92289 is bad:
           The primary key is not live
  because: Expired on 2022-09-08T13:11:47Z
rc=1
```

