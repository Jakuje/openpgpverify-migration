# Keyring update from upstream for btrfs-progs

**Status: proposed**

Failing call: `--keyring=/builddir/new/gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg --signature=/builddir/new/btrfs-progs-v7.1.tar.sign --data=-`

Phase 1 reason: `expired`

## gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg

- from: https://git.kernel.org/pub/scm/docs/kernel/pgpkeys.git/plain/keys/C565D5F9D76D583B.asc
- **renamed to `C565D5F9D76D583B.asc`; its `Source` line becomes the URL**
- certificates (unchanged): F2B41200C54EFB30380C1756C565D5F9D76D583B
- size: 4037 → 9137 bytes

```
curl -fsSL -O https://git.kernel.org/pub/scm/docs/kernel/pgpkeys.git/plain/keys/C565D5F9D76D583B.asc
```

```diff
--- dist-git/gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg
+++ upstream/gpgkey-F2B41200C54EFB30380C1756C565D5F9D76D583B.gpg
@@ -1,13 +1,12 @@
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
+self-signatures PositiveCertification: 2024-01-12
 self-signatures SubkeyBinding: 2014-08-27
+third-party PositiveCertification: 1
```

Host verification skipped (data from stdin or a generated file); run phase1.py after approval.

