# Keyring refresh for ncurses

**Status: proposed**

Failing call: `--keyring=/builddir/new/dickey@invisible-island.net-rsa3072.asc --signature=/builddir/new/ncurses-6.6.tar.gz.asc --data=/builddir/new/ncurses-6.6.tar.gz`

Phase 1 reason: `expired`

## dickey@invisible-island.net-rsa3072.asc

- certificates: 19882D92DDA4C400C22C0D56CC2AF4472167BE03
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 2505 → 12978 bytes

```diff
--- dist-git/dickey@invisible-island.net-rsa3072.asc
+++ refreshed/dickey@invisible-island.net-rsa3072.asc
@@ -1,11 +1,12 @@
       Fingerprint: 19882D92DDA4C400C22C0D56CC2AF4472167BE03
-                   Invalid: The primary key is not live: Expired on 2023-07-30T23:08:24Z
-  Expiration time: 2023-07-30 23:08:24 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2029-04-02 01:56:22 UTC (creation time + 7years 8months 1day 20h 19m 10s)
         Key flags: certification, signing
            Subkey: 711EBE244DE66E56020CCB474C5C495AB79670BF
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2023-07-30T23:08:24Z
-  Expiration time: 2023-07-30 23:08:24 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2029-04-02 01:57:11 UTC (creation time + 7years 8months 1day 20h 19m 59s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Thomas E. Dickey (self-signed w/o SHA1) <dickey@invisible-island.net>
-self-signatures PositiveCertification: 2021-07-30
-self-signatures SubkeyBinding: 2021-07-30
+           UserID: Thomas E. Dickey (use for email) <dickey@his.com>
+self-signatures PositiveCertification: 2021-07-30, 2022-01-31, 2022-10-31, 2023-12-10, 2026-01-18
+self-signatures SubkeyBinding: 2021-07-30, 2022-10-31, 2023-12-10, 2026-01-18
+third-party CasualCertification: 1
+third-party GenericCertification: 2
```

## Verification with the refreshed keyring

```
$ sqv ... ncurses-6.6.tar.gz
19882D92DDA4C400C22C0D56CC2AF4472167BE03
rc=0
```

