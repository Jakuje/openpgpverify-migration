# Keyring refresh for btrfs-progs

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg --signature=/builddir/new/btrfs-progs-v7.1.tar.sign --data=-`

Phase 1 reason: `expired`

## gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg

- certificates: F2B41200C54EFB30380C1756C565D5F9D76D583B
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com; hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com, WKD; hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 4037 → 28009 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network search --output - F2B41200C54EFB30380C1756C565D5F9D76D583B \
  | sq keyring filter --experimental --cert F2B41200C54EFB30380C1756C565D5F9D76D583B --output update.pgp
sq keyring merge gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg update.pgp | sq packet dearmor --output gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg.new
mv gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg.new gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg
```

```diff
--- dist-git/gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg
+++ refreshed/gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg
@@ -1,13 +1,13 @@
       Fingerprint: F2B41200C54EFB30380C1756C565D5F9D76D583B
-                   Invalid: The primary key is not live: Expired on 2024-08-24T18:40:54Z
-  Expiration time: 2024-08-24 18:40:54 UTC (creation time + 9years 11months 27days 21h 50m 24s)
+  Expiration time: 2034-01-09 00:19:59 UTC (creation time + 19years 4months 12days 17h 24m 41s)
         Key flags: certification, signing
            Subkey: 4421024497B071710005477564AE64A9A61BB5A1
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2024-08-24T18:40:54Z
         Key flags: transport encryption, data-at-rest encryption
            UserID: David Sterba <dave@jikos.cz>
            UserID: David Sterba <dsterba@suse.com>
            UserID: David Sterba <dsterba@suse.cz>
            UserID: David Sterba <kdave@kernel.org>
-self-signatures PositiveCertification: 2014-08-27, 2014-09-12
+self-signatures PositiveCertification: 2014-08-27, 2014-09-12, 2023-09-14, 2024-01-12
 self-signatures SubkeyBinding: 2014-08-27
+third-party GenericCertification: 5
+third-party PositiveCertification: 1
```

Host verification skipped (data from stdin or a generated file); run phase1.py after approval.

