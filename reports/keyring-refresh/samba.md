# Keyring refresh for samba

**Status: proposed**

Failing call: `--keyring=/builddir/new/samba-pubkey_AA99442FB680B620.gpg --signature=/builddir/new/samba-4.25.1.tar.asc --data=-`

Phase 1 reason: `expired`

## samba-pubkey_AA99442FB680B620.gpg

- certificates: 81F5E2832BD2545A1897B713AA99442FB680B620
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD
- size: 2290 → 7105 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network search --output - 81F5E2832BD2545A1897B713AA99442FB680B620 \
  | sq keyring filter --experimental --cert 81F5E2832BD2545A1897B713AA99442FB680B620 --output update.pgp
sq keyring merge samba-pubkey_AA99442FB680B620.gpg update.pgp | sq packet dearmor --output samba-pubkey_AA99442FB680B620.gpg.new
mv samba-pubkey_AA99442FB680B620.gpg.new samba-pubkey_AA99442FB680B620.gpg
```

```diff
--- dist-git/samba-pubkey_AA99442FB680B620.gpg
+++ refreshed/samba-pubkey_AA99442FB680B620.gpg
@@ -1,11 +1,10 @@
       Fingerprint: 81F5E2832BD2545A1897B713AA99442FB680B620
-                   Invalid: The primary key is not live: Expired on 2022-12-21T12:11:00Z
-  Expiration time: 2022-12-21 12:11:00 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2027-12-12 17:06:40 UTC (creation time + 6years 11months 20days 20h 46m 4s)
         Key flags: certification, signing
            Subkey: 8ECB3E1AD3C66464249027DE97EF9386FBFD4002
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2022-12-21T12:11:00Z
-  Expiration time: 2022-12-21 12:11:00 UTC (creation time + 1year 11months 29days 21h 50m 24s)
+  Expiration time: 2027-12-12 17:09:32 UTC (creation time + 6years 11months 20days 20h 48m 56s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Samba Distribution Verification Key <samba-bugs@samba.org>
-self-signatures PositiveCertification: 2020-12-21
-self-signatures SubkeyBinding: 2020-12-21
+self-signatures PositiveCertification: 2020-12-21, 2022-12-19, 2023-12-18, 2024-10-15, 2025-12-12
+self-signatures SubkeyBinding: 2020-12-21, 2022-12-19, 2023-12-18, 2024-10-15, 2025-12-12
+third-party GenericCertification: 1
```

Host verification skipped (data from stdin or a generated file); run phase1.py after approval.

