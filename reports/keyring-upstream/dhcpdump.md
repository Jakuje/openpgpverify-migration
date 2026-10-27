# Keyring update from upstream for dhcpdump

**Status: proposed**

Failing call: `--keyring=/builddir/new/signing-key.asc --signature=/builddir/new/dhcpdump-2.00.tar.xz.asc --data=/builddir/new/dhcpdump-2.00.tar.xz`

Phase 1 reason: `expired`

## signing-key.asc

- from: https://raw.githubusercontent.com/bbonev/dhcpdump/v2.00/debian/upstream/signing-key.asc
- certificates (unchanged): BA60BC20F37E59444D6D25001365720913D2F22D
- size: 10463 → 11320 bytes

```
curl -fsSL -o signing-key.asc https://raw.githubusercontent.com/bbonev/dhcpdump/v2.00/debian/upstream/signing-key.asc
```

```diff
--- dist-git/signing-key.asc
+++ upstream/signing-key.asc
@@ -1,13 +1,12 @@
       Fingerprint: BA60BC20F37E59444D6D25001365720913D2F22D
-                   Invalid: The primary key is not live: Expired on 2023-01-30T18:12:31Z
-  Expiration time: 2023-01-30 18:12:31 UTC (creation time + 2years 7months 3days 5h 15m 7s)
+  Expiration time: 2028-01-21 06:00:35 UTC (creation time + 7years 6months 23days 21h 36m 47s)
         Key flags: certification, signing
            Subkey: 5A7BF57ECE76D83A42B1CA620F9A14812426B4F9
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2023-01-30T18:12:31Z
-  Expiration time: 2023-01-30 18:13:04 UTC (creation time + 2years 7months 3days 5h 15m 40s)
+  Expiration time: 2028-01-21 06:00:17 UTC (creation time + 7years 6months 23days 21h 36m 29s)
         Key flags: transport encryption, data-at-rest encryption
+           UserID: Boian Bonev <bbonev@devuan.org>
            UserID: Boian Bonev <bbonev@ipacct.com>
            UserID: Boian Bonev <boian@bonev.com>
            UserID: Boian Bonev <ipacct@gmail.com>
-self-signatures PositiveCertification: 2021-01-30, 2021-02-01
-self-signatures SubkeyBinding: 2021-01-30
+self-signatures PositiveCertification: 2026-01-21
+self-signatures SubkeyBinding: 2026-01-21
```

## Verification with the upstream keyring

```
$ sqv ... dhcpdump-2.00.tar.xz
BA60BC20F37E59444D6D25001365720913D2F22D
rc=0
```

