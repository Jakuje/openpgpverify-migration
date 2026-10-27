# Keyring refresh for expat

**Status: proposed**

Failing call: `--keyring=/builddir/new/3176EF7DB2367F1FCA4F306B1F9B0E909AF37285 --signature=/builddir/new/expat-2.8.5.tar.gz.asc --data=/builddir/new/expat-2.8.5.tar.gz`

Phase 1 reason: `expired`

## 3176EF7DB2367F1FCA4F306B1F9B0E909AF37285

- certificates: 3176EF7DB2367F1FCA4F306B1F9B0E909AF37285
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 14920 → 30743 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network search --output - 3176EF7DB2367F1FCA4F306B1F9B0E909AF37285 \
  | sq keyring filter --experimental --cert 3176EF7DB2367F1FCA4F306B1F9B0E909AF37285 --output update.pgp
sq keyring merge --output 3176EF7DB2367F1FCA4F306B1F9B0E909AF37285.new 3176EF7DB2367F1FCA4F306B1F9B0E909AF37285 update.pgp
mv 3176EF7DB2367F1FCA4F306B1F9B0E909AF37285.new 3176EF7DB2367F1FCA4F306B1F9B0E909AF37285
```

```diff
--- dist-git/3176EF7DB2367F1FCA4F306B1F9B0E909AF37285
+++ refreshed/3176EF7DB2367F1FCA4F306B1F9B0E909AF37285
@@ -1,15 +1,15 @@
       Fingerprint: 3176EF7DB2367F1FCA4F306B1F9B0E909AF37285
-                   Invalid: The primary key is not live: Expired on 2026-01-04T15:35:59Z
-  Expiration time: 2026-01-04 15:35:59 UTC (creation time + 6years 7months 27days 7h 16m 34s)
+  Expiration time: 2026-12-28 19:31:59 UTC (creation time + 7years 7months 20days 5h 12m 34s)
         Key flags: certification, signing
            Subkey: CB8DE70A90CFBF6C3BF5CC5696262ACFFBD3AEC6
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-01-04T15:35:59Z
-  Expiration time: 2026-01-04 15:36:42 UTC (creation time + 6years 7months 27days 7h 8m 45s)
+  Expiration time: 2026-12-28 19:32:44 UTC (creation time + 7years 7months 20days 5h 4m 47s)
         Key flags: signing
            Subkey: A10DAC3EE122F79957D65403BF9802AEE9F129C3
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-01-04T15:35:59Z
-  Expiration time: 2026-01-04 15:36:42 UTC (creation time + 6years 7months 27days 7h 17m 17s)
+  Expiration time: 2026-12-28 19:32:44 UTC (creation time + 7years 7months 20days 5h 13m 19s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Sebastian Pipping <sping@gentoo.org>
-self-signatures PositiveCertification: 2019-05-09, 2022-01-02, 2023-01-17, 2024-01-05
-self-signatures SubkeyBinding: 2019-05-09, 2022-01-02, 2023-01-17, 2024-01-05
+self-signatures PositiveCertification: 2019-05-09, 2020-05-06, 2021-04-29, 2022-01-02, 2023-01-17, 2024-01-05, 2025-12-28
+self-signatures SubkeyBinding: 2019-05-09, 2021-04-29, 2022-01-02, 2023-01-17, 2024-01-05, 2025-12-28
+third-party CertificationRevocation: 7
+third-party GenericCertification: 15
+third-party PositiveCertification: 2
```

## Verification with the refreshed keyring

```
$ sqv ... expat-2.8.5.tar.gz
3176EF7DB2367F1FCA4F306B1F9B0E909AF37285
rc=0
```

