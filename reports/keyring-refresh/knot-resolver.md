# Keyring refresh for knot-resolver

**Status: proposed**

Failing call: `--keyring=/builddir/new/kresd-keyblock.asc --signature=/builddir/new/knot-resolver-5.7.9.tar.xz.asc --data=/builddir/new/knot-resolver-5.7.9.tar.xz`

Phase 1 reason: `expired`

## kresd-keyblock.asc

- certificates: 3057EE9A448F362D74205A779AB120DA0A76F6DE, B6006460B60A80E782062449E747DF1F9575A3AA
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 8009 → 22362 bytes

```diff
--- dist-git/kresd-keyblock.asc
+++ refreshed/kresd-keyblock.asc
@@ -1,10 +1,8 @@
       Fingerprint: 3057EE9A448F362D74205A779AB120DA0A76F6DE
-                   Invalid: The primary key is not live: Expired on 2024-03-06T15:32:20Z
-  Expiration time: 2024-03-06 15:32:20 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2030-02-03 23:00:00 UTC (creation time + 7years 10months 29days 3h 51m 40s)
         Key flags: certification, signing
            Subkey: A5170E99CFCA7ED34200C52CCF853D657BD054EC
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2024-03-06T15:32:20Z
-  Expiration time: 2024-03-06 15:32:20 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2030-02-03 23:00:00 UTC (creation time + 7years 10months 29days 3h 51m 40s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Ales Mrazek <ales.mrazek@nic.cz>
       Fingerprint: B6006460B60A80E782062449E747DF1F9575A3AA
@@ -16,5 +14,8 @@
            UserID: Vladimír Čunát (personal) <v@cunat.cz>
            UserID: Vladimír Čunát (work) <vladimir.cunat@nic.cz>
            UserID: Vladimír Čunát <vcunat@gmail.com>
-self-signatures PositiveCertification: 2021-10-13, 2022-03-07
-self-signatures SubkeyBinding: 2021-10-13, 2022-03-07
+self-signatures PositiveCertification: 2016-10-16, 2017-09-21, 2017-09-25, 2017-11-16, 2019-02-24, 2021-10-13, 2022-03-07, 2024-03-04, 2026-02-04
+self-signatures SubkeyBinding: 2016-10-16, 2021-10-13, 2022-03-07, 2024-03-04, 2026-02-04
+third-party CasualCertification: 1
+third-party GenericCertification: 1
+third-party PositiveCertification: 1
```

## Verification with the refreshed keyring

```
$ sqv ... knot-resolver-5.7.9.tar.xz
3057EE9A448F362D74205A779AB120DA0A76F6DE
rc=0
```

