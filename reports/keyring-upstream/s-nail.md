# Keyring update from upstream for s-nail

**Status: still-fails**

Failing call: `--keyring=/builddir/new/steffen.asc --signature=/builddir/new/s-nail-14.9.25.tar.xz.asc --data=/builddir/new/s-nail-14.9.25.tar.xz`

Phase 1 reason: `sha1-cert`

## steffen.asc

- from: https://ftp.sdaoden.eu/steffen.asc
- certificates (unchanged): EE19E1C1F2F7054F8D3954D8308964B51883A0DD
- size: 3817 → 5288 bytes

```
curl -fsSL -o steffen.asc https://ftp.sdaoden.eu/steffen.asc
```

```diff
--- dist-git/steffen.asc
+++ upstream/steffen.asc
@@ -1,11 +1,13 @@
       Fingerprint: EE19E1C1F2F7054F8D3954D8308964B51883A0DD
-                   Invalid: No binding signature at time 2026-10-27T11:31:39Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+  Expiration time: 2031-12-27 18:33:03 UTC (creation time + 14years 26days 10h 22m 25s)
+        Key flags: certification, signing
+           Subkey: 053B280D8B57274E2342D4ED5E8DB724A57802DD
+  Expiration time: 2030-12-27 18:33:18 UTC (creation time + 13years 26days 16h 22m 40s)
+        Key flags: transport encryption, data-at-rest encryption
            Subkey: 8A2A4D609FDC539C75F55B95DF082F6AEEC8C2FF
-                   Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
+                   Invalid: Policy rejected non-revocation signature (PrimaryKeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-27T11:31:39Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: Policy rejected non-revocation signature (PrimaryKeyBinding) requiring second pre-image resistance: SHA1 is not considered secure
            UserID: Steffen Nurpmeso <steffen@sdaoden.eu>
-                   Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
-                   because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2018-06-02
-self-signatures SubkeyBinding: 2018-06-02
+self-signatures PositiveCertification: 2020-12-29
+self-signatures SubkeyBinding: 2020-12-29
```

## Verification with the upstream keyring

```
$ sqv ... s-nail-14.9.25.tar.xz
Signing key on EE19E1C1F2F7054F8D3954D8308964B51883A0DD is not bound:
           Policy rejected non-revocation signature (PrimaryKeyBinding) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

