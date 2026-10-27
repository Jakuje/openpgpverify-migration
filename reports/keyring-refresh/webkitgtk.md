# Keyring refresh for webkitgtk

**Status: proposed**

Failing call: `--keyring=/builddir/new/webkitgtk-keys.gpg --signature=/builddir/new/webkitgtk-2.54.2.tar.xz.asc --data=/builddir/new/webkitgtk-2.54.2.tar.xz`

Phase 1 reason: `expired`

## webkitgtk-keys.gpg

- certificates: 013A0127AC9C65B34FFA62526C1009B693975393, 5AA3BC334FD7E3369E7C77B291C559DBE4C9123B
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 4178 → 13549 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network search --output - 013A0127AC9C65B34FFA62526C1009B693975393 5AA3BC334FD7E3369E7C77B291C559DBE4C9123B \
  | sq keyring filter --experimental --cert 013A0127AC9C65B34FFA62526C1009B693975393 --cert 5AA3BC334FD7E3369E7C77B291C559DBE4C9123B --output update.pgp
sq keyring merge webkitgtk-keys.gpg update.pgp | sq packet dearmor --output webkitgtk-keys.gpg.new
mv webkitgtk-keys.gpg.new webkitgtk-keys.gpg
```

```diff
--- dist-git/webkitgtk-keys.gpg
+++ refreshed/webkitgtk-keys.gpg
@@ -1,19 +1,17 @@
       Fingerprint: 013A0127AC9C65B34FFA62526C1009B693975393
-                   Invalid: The primary key is not live: Expired on 2026-04-09T10:58:53Z
-  Expiration time: 2026-04-09 10:58:53 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2028-04-19 07:53:36 UTC (creation time + 4years 9days 20h 54m 43s)
         Key flags: certification, signing
            Subkey: 5FB4EC8D6401C26F72B7B559B92AE30C7A82B686
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2026-04-09T10:58:53Z
-  Expiration time: 2026-04-09 10:58:53 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2028-04-19 07:57:41 UTC (creation time + 4years 9days 20h 58m 48s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Carlos Garcia Campos <cgarcia@igalia.com>
       Fingerprint: 5AA3BC334FD7E3369E7C77B291C559DBE4C9123B
                    Invalid: Policy rejected asymmetric algorithm: DSA1024 is not considered secure
            Subkey: 86578FD638E90525130ADF4976D146E5CE5D1038
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
                    Invalid: primary key: Policy rejected asymmetric algorithm, because DSA1024 is not considered secure
            UserID: Adrián Pérez de Castro (personal) <adrian@perezdecastro.org>
            UserID: Adrián Pérez de Castro <aperez@igalia.com>
-self-signatures PositiveCertification: 2024-04-09, 2024-04-14
-self-signatures SubkeyBinding: 2008-06-02, 2024-04-09
+self-signatures PositiveCertification: 2008-06-02, 2015-07-16, 2016-05-11, 2018-05-12, 2020-05-12, 2022-05-11, 2024-04-09, 2024-04-14, 2026-03-16, 2026-04-20
+self-signatures SubkeyBinding: 2008-06-02, 2024-04-09, 2026-03-16, 2026-04-20
+third-party CasualCertification: 1
+third-party GenericCertification: 13
```

## Verification with the refreshed keyring

```
$ sqv ... webkitgtk-2.54.2.tar.xz
013A0127AC9C65B34FFA62526C1009B693975393
rc=0
```

