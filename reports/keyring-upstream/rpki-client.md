# Keyring update from upstream for rpki-client

**Status: proposed**

Failing call: `--keyring=/builddir/new/B5B6416FEA6DDA05EA562A9FCB987F2783972FF9 --signature=/builddir/new/rpki-client-9.9.tar.gz.asc --data=/builddir/new/rpki-client-9.9.tar.gz`

Phase 1 reason: `expired`

## B5B6416FEA6DDA05EA562A9FCB987F2783972FF9

- from: https://keys.openpgp.org/vks/v1/by-fingerprint/B5B6416FEA6DDA05EA562A9FCB987F2783972FF9
- certificates (unchanged): B5B6416FEA6DDA05EA562A9FCB987F2783972FF9
- size: 1817 → 3438 bytes

```
curl -fsSL -o B5B6416FEA6DDA05EA562A9FCB987F2783972FF9 https://keys.openpgp.org/vks/v1/by-fingerprint/B5B6416FEA6DDA05EA562A9FCB987F2783972FF9
```

```diff
--- dist-git/B5B6416FEA6DDA05EA562A9FCB987F2783972FF9
+++ upstream/B5B6416FEA6DDA05EA562A9FCB987F2783972FF9
@@ -1,6 +1,5 @@
       Fingerprint: B5B6416FEA6DDA05EA562A9FCB987F2783972FF9
-                   Invalid: The primary key is not live: Expired on 2026-03-18T18:43:06Z
-  Expiration time: 2026-03-18 18:43:06 UTC (creation time + 5years 11months 3days 18h 38m 33s)
+  Expiration time: 2028-04-13 19:57:07 UTC (creation time + 7years 11months 30days 7h 52m 34s)
         Key flags: certification, signing
            UserID: Sebastian Benoit (software signing only) <benno@openbsd.org>
-self-signatures PositiveCertification: 2023-03-19
+self-signatures PositiveCertification: 2021-04-15, 2023-03-19, 2026-04-14
```

## Verification with the upstream keyring

```
$ sqv ... rpki-client-9.9.tar.gz
B5B6416FEA6DDA05EA562A9FCB987F2783972FF9
rc=0
```

