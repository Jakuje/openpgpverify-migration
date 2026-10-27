# Keyring refresh for aide

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-aide.gpg --signature=/builddir/new/aide-0.19.4.tar.gz.asc --data=/builddir/new/aide-0.19.4.tar.gz`

Phase 1 reason: `expired`

## gpgkey-aide.gpg

- certificates: 2BBBD30FAAB29B3253BCFBA6F6947DAB68E7B931
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keys.openpgp.org, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 5160 → 59219 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network search --output - 2BBBD30FAAB29B3253BCFBA6F6947DAB68E7B931 \
  | sq keyring filter --experimental --cert 2BBBD30FAAB29B3253BCFBA6F6947DAB68E7B931 --output update.pgp
sq keyring merge gpgkey-aide.gpg update.pgp | sq packet dearmor --output gpgkey-aide.gpg.new
mv gpgkey-aide.gpg.new gpgkey-aide.gpg
```

```diff
--- dist-git/gpgkey-aide.gpg
+++ refreshed/gpgkey-aide.gpg
@@ -1,20 +1,19 @@
       Fingerprint: 2BBBD30FAAB29B3253BCFBA6F6947DAB68E7B931
-                   Invalid: The primary key is not live: Expired on 2026-06-27T05:58:55Z
-  Expiration time: 2026-06-27 05:58:55 UTC (creation time + 14years 11months 29days 5h 43m 31s)
+  Expiration time: 2028-06-27 07:14:25 UTC (creation time + 16years 11months 29days 18h 59m 1s)
         Key flags: certification
            Subkey: 5495CDA17C9AC17AB23841A718EE86386022EF57
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-06-27T05:58:55Z
-  Expiration time: 2025-06-27 06:00:19 UTC (creation time + 13years 11months 29days 11h 42m 25s)
+  Expiration time: 2027-06-27 07:15:04 UTC (creation time + 15years 11months 29days 57m 10s)
         Key flags: signing
            Subkey: A6CCE790DD1E6669B7CD501057C198E495A601C7
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-06-27T05:58:55Z
-  Expiration time: 2025-06-27 06:00:51 UTC (creation time + 13years 11months 29days 11h 39m 43s)
+  Expiration time: 2027-06-27 07:15:19 UTC (creation time + 15years 11months 29days 54m 11s)
         Key flags: transport encryption, data-at-rest encryption
            Subkey: E22E962797F39BD6927E4AEDF4B483CB268B1790
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-06-27T05:58:55Z
-  Expiration time: 2025-06-27 06:00:51 UTC (creation time + 13years 11months 29days 11h 37m 42s)
+  Expiration time: 2027-06-27 07:15:32 UTC (creation time + 15years 11months 29days 52m 23s)
         Key flags: authentication
            UserID: Hannes von Haugwitz <hannes@vonhaugwitz.com>
            UserID: Hannes von Haugwitz <hvhaugwitz@debian.org>
-self-signatures PositiveCertification: 2023-06-04
-self-signatures SubkeyBinding: 2023-06-04
+self-signatures PositiveCertification: 2011-06-28, 2013-10-27, 2015-06-25, 2019-01-12, 2021-02-14, 2023-06-04, 2025-04-28, 2026-06-07
+self-signatures SubkeyBinding: 2011-06-28, 2013-05-09, 2015-06-25, 2017-07-01, 2019-01-12, 2021-02-14, 2023-06-04, 2025-04-28, 2026-06-07
+third-party CasualCertification: 2
+third-party GenericCertification: 20
+third-party PositiveCertification: 3
```

## Verification with the refreshed keyring

```
$ sqv ... aide-0.19.4.tar.gz
2BBBD30FAAB29B3253BCFBA6F6947DAB68E7B931
rc=0
```

