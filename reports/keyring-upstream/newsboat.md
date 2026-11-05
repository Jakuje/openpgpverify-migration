# Keyring update from upstream for newsboat

**Status: proposed**

Failing call: `--keyring=/builddir/new/newsboat.pgp --signature=/builddir/new/newsboat-2.45.tar.xz.asc --data=/builddir/new/newsboat-2.45.tar.xz`

Phase 1 reason: `expired`

## newsboat.pgp

- from: https://keys.openpgp.org/vks/v1/by-fingerprint/B8B1756A0DDBF0760CE67CCF4ED6CD61932B9EBE#/newsboat.asc
- **renamed to `newsboat.asc`; its `Source` line becomes the URL**
- certificates (unchanged): B8B1756A0DDBF0760CE67CCF4ED6CD61932B9EBE
- size: 7173 → 9700 bytes

```
curl -fsSL -o newsboat.asc 'https://keys.openpgp.org/vks/v1/by-fingerprint/B8B1756A0DDBF0760CE67CCF4ED6CD61932B9EBE'
```

```diff
--- dist-git/newsboat.pgp
+++ upstream/newsboat.pgp
@@ -5,6 +5,5 @@
   Expiration time: 2027-10-17 12:06:26 UTC (creation time + 10years 29days 10h 4m 55s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: Newsboat project <newsboat@googlegroups.com>
-self-signatures PositiveCertification: 2017-09-17, 2020-09-20, 2021-09-20, 2022-09-25, 2026-10-04
-self-signatures SubkeyBinding: 2026-10-04
-third-party PositiveCertification: 1
+self-signatures PositiveCertification: 2017-09-17, 2020-09-20, 2021-09-20, 2022-09-25, 2023-09-28, 2025-09-21, 2026-10-04
+self-signatures SubkeyBinding: 2023-09-28, 2025-09-21, 2026-10-04
```

## Verification with the upstream keyring

```
$ sqv ... newsboat-2.45.tar.xz
B8B1756A0DDBF0760CE67CCF4ED6CD61932B9EBE
rc=0
```

