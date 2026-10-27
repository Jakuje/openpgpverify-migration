# Keyring update from upstream for opam

**Status: proposed**

Failing call: `--data=/builddir/new/opam-full-2.6.1.tar.gz --signature=/builddir/new/opam-full-2.6.1.tar.gz.sig --keyring=/builddir/new/opam-dev-pubkey.pgp`

Phase 1 reason: `expired`

## opam-dev-pubkey.pgp

- from: https://opam.ocaml.org/opam-dev-pubkey.pgp
- certificates (unchanged): 92C526AE50DF39470EB2911BED4CF1CA67CBAA92
- size: 3143 → 3143 bytes

```
curl -fsSL -o opam-dev-pubkey.pgp https://opam.ocaml.org/opam-dev-pubkey.pgp
```

```diff
--- dist-git/opam-dev-pubkey.pgp
+++ upstream/opam-dev-pubkey.pgp
@@ -1,11 +1,10 @@
       Fingerprint: 92C526AE50DF39470EB2911BED4CF1CA67CBAA92
-                   Invalid: The primary key is not live: Expired on 2025-05-19T13:07:29Z
-  Expiration time: 2025-05-19 13:07:29 UTC (creation time + 4years 8months 27days 12h 29m 57s)
+  Expiration time: 2027-02-04 10:06:40 UTC (creation time + 6years 5months 14days 5h 9m 56s)
         Key flags: certification, signing
            Subkey: F68C586276DF0EDE181B3B073C33809E7E2CA45D
-                   Invalid: The certificate is not live: The primary key is not live, because Expired on 2025-05-19T13:07:29Z
+                   Invalid: The subkey is not live: Expired on 2024-07-16T10:58:55Z
   Expiration time: 2024-07-16 10:58:55 UTC (creation time + 3years 10months 24days 19h 14m 11s)
         Key flags: transport encryption, data-at-rest encryption
            UserID: opam dev team <opam@ocaml.org>
-self-signatures PositiveCertification: 2024-08-22
+self-signatures PositiveCertification: 2026-04-10
 self-signatures SubkeyBinding: 2024-01-18
```

## Verification with the upstream keyring

```
$ sqv ... opam-full-2.6.1.tar.gz
92C526AE50DF39470EB2911BED4CF1CA67CBAA92
rc=0
```

