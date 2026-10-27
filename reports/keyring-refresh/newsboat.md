# Keyring refresh for newsboat

**Status: proposed**

Failing call: `--keyring=/builddir/new/newsboat.pgp --signature=/builddir/new/newsboat-2.45.tar.xz.asc --data=/builddir/new/newsboat-2.45.tar.xz`

Phase 1 reason: `expired`

## newsboat.pgp

- certificates: B8B1756A0DDBF0760CE67CCF4ED6CD61932B9EBE
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 7173 → 15164 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network search --output - B8B1756A0DDBF0760CE67CCF4ED6CD61932B9EBE \
  | sq keyring filter --experimental --cert B8B1756A0DDBF0760CE67CCF4ED6CD61932B9EBE --output update.pgp
sq keyring merge --output newsboat.pgp.new newsboat.pgp update.pgp
mv newsboat.pgp.new newsboat.pgp
```

```diff
--- dist-git/newsboat.pgp
+++ refreshed/newsboat.pgp
@@ -5,6 +5,7 @@
   Expiration time: 2027-10-17 12:06:26 UTC (creation time + 10years 29days 10h 4m 55s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Newsboat project <newsboat@googlegroups.com>
-self-signatures PositiveCertification: 2017-09-17, 2020-09-20, 2021-09-20, 2022-09-25, 2026-10-04
-self-signatures SubkeyBinding: 2026-10-04
+self-signatures PositiveCertification: 2017-09-17, 2020-09-20, 2021-09-20, 2022-09-25, 2023-09-28, 2025-09-21, 2026-10-04
+self-signatures SubkeyBinding: 2017-09-17, 2020-09-20, 2021-09-20, 2022-09-25, 2023-09-28, 2025-09-21, 2026-10-04
+third-party GenericCertification: 3
 third-party PositiveCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... newsboat-2.45.tar.xz
B8B1756A0DDBF0760CE67CCF4ED6CD61932B9EBE
rc=0
```

