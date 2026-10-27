# Keyring refresh for mat2

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.gpg --signature=/builddir/new/0.14.0.tar.gz.asc --data=/builddir/new/mat2-0.14.0.tar.gz`

Phase 1 reason: `expired`

## gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.gpg

- certificates: 9FCDEE9E1A381F311EA62A7404D041E8171901CC
- found via: hkps://keys.mailvelope.com, hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 3458 → 21737 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network search --output - 9FCDEE9E1A381F311EA62A7404D041E8171901CC \
  | sq keyring filter --experimental --cert 9FCDEE9E1A381F311EA62A7404D041E8171901CC --output update.pgp
sq keyring merge gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.gpg update.pgp | sq packet dearmor --output gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.gpg.new
mv gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.gpg.new gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.gpg
```

```diff
--- dist-git/gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.gpg
+++ refreshed/gpgkey-9FCDEE9E1A381F311EA62A7404D041E8171901CC.gpg
@@ -1,16 +1,15 @@
       Fingerprint: 9FCDEE9E1A381F311EA62A7404D041E8171901CC
-                   Invalid: The primary key is not live: Expired on 2020-07-23T17:21:36Z
-  Expiration time: 2020-07-23 17:21:36 UTC (creation time + 4years 11months 29days 3h 50m 24s)
+  Expiration time: 2030-07-15 22:00:00 UTC (creation time + 14years 11months 20days 20h 28m 48s)
         Key flags: certification, signing
            Subkey: 0CB250E28DD3BB8EFA4553E4AC28F00D0351B960
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2020-07-23T17:21:36Z
-  Expiration time: 2020-07-23 17:21:36 UTC (creation time + 4years 11months 29days 3h 50m 24s)
+  Expiration time: 2030-07-15 22:00:00 UTC (creation time + 14years 11months 20days 20h 28m 48s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Julien (jvoisin) Voisin <julien.voisin@dustri.org>
            UserID: Julien (jvoisin) Voisin <jvoisin@openmailbox.net>
                    Revoked:
-                   Invalid: No binding signature at time 2026-10-27T10:59:29Z
            UserID: Julien (jvoisin) Voisin <jvoisin@riseup.net>
 self-signatures CertificationRevocation: 2016-08-17
-self-signatures PositiveCertification: 2015-07-25, 2015-08-02
-self-signatures SubkeyBinding: 2015-07-25
+self-signatures PositiveCertification: 2015-07-25, 2015-08-02, 2020-04-25, 2020-07-14, 2024-11-08, 2025-04-28, 2025-07-16
+self-signatures SubkeyBinding: 2015-07-25, 2020-07-14, 2025-07-16
+third-party GenericCertification: 6
+third-party PositiveCertification: 2
```

## Verification with the refreshed keyring

```
$ sqv ... mat2-0.14.0.tar.gz
9FCDEE9E1A381F311EA62A7404D041E8171901CC
rc=0
```

