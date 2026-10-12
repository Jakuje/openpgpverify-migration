# Keyring refresh for mpdscribble

**Status: no-update**

Failing call: `--keyring=/builddir/new/0392335A78083894A4301C43236E8A58C6DB4512.gpg --signature=/builddir/new/mpdscribble-0.25.tar.xz.sig --data=/builddir/new/mpdscribble-0.25.tar.xz`

Phase 1 reason: `sha1-cert`

## 0392335A78083894A4301C43236E8A58C6DB4512.gpg

- certificates: 0392335A78083894A4301C43236E8A58C6DB4512
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 5523 → 5523 bytes

```diff
--- dist-git/0392335A78083894A4301C43236E8A58C6DB4512.gpg
+++ refreshed/0392335A78083894A4301C43236E8A58C6DB4512.gpg
@@ -1,9 +1,9 @@
       Fingerprint: 0392335A78083894A4301C43236E8A58C6DB4512
-                   Invalid: No binding signature at time 2026-10-12T11:55:46Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: No binding signature at time 2026-10-12T11:55:47Z: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
            Subkey: F1779854149CFAD68E2A07B16080A3C3376AFD81
                    Invalid: Policy rejected non-revocation signature (SubkeyBinding) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-                   Invalid: primary key: No binding signature at time 2026-10-12T11:55:46Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
+                   Invalid: primary key: No binding signature at time 2026-10-12T11:55:47Z, because Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance, because SHA1 is not considered secure
            UserID: Max Kellermann <max@blarg.de>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
```

