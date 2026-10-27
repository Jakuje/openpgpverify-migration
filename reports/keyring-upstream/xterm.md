# Keyring update from upstream for xterm

**Status: proposed**

Failing call: `--keyring=/builddir/new/dickey@invisible-island.net-rsa3072.asc --signature=/builddir/new/xterm-411.tgz.asc --data=/builddir/new/xterm-411.tgz`

Phase 1 reason: `expired`

## dickey@invisible-island.net-rsa3072.asc

- from: https://invisible-island.net/public/dickey@invisible-island.net-rsa3072.asc
- certificates (unchanged): 19882D92DDA4C400C22C0D56CC2AF4472167BE03
- size: 5479 → 5479 bytes

```
curl -fsSL -o dickey@invisible-island.net-rsa3072.asc https://invisible-island.net/public/dickey@invisible-island.net-rsa3072.asc
```

```diff
--- dist-git/dickey@invisible-island.net-rsa3072.asc
+++ upstream/dickey@invisible-island.net-rsa3072.asc
@@ -1,13 +1,11 @@
       Fingerprint: 19882D92DDA4C400C22C0D56CC2AF4472167BE03
-                   Invalid: The primary key is not live: Expired on 2026-01-18T23:06:45Z
-  Expiration time: 2026-01-18 23:06:45 UTC (creation time + 4years 5months 19days 19h 10m 21s)
+  Expiration time: 2029-04-02 01:56:22 UTC (creation time + 7years 8months 1day 20h 19m 10s)
         Key flags: certification, signing
            Subkey: 711EBE244DE66E56020CCB474C5C495AB79670BF
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-01-18T23:06:45Z
-  Expiration time: 2026-01-18 23:07:00 UTC (creation time + 4years 5months 19days 19h 10m 36s)
+  Expiration time: 2029-04-02 01:57:11 UTC (creation time + 7years 8months 1day 20h 19m 59s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Thomas E. Dickey (self-signed w/o SHA1) <dickey@invisible-island.net>
            UserID: Thomas E. Dickey (use for email) <dickey@his.com>
-self-signatures PositiveCertification: 2023-12-10
-self-signatures SubkeyBinding: 2023-12-10
+self-signatures PositiveCertification: 2026-01-18
+self-signatures SubkeyBinding: 2026-01-18
 third-party GenericCertification: 1
```

## Verification with the upstream keyring

```
$ sqv ... xterm-411.tgz
19882D92DDA4C400C22C0D56CC2AF4472167BE03
rc=0
```

