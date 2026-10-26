# Keyring refresh for mpd

**Status: no-update**

Failing call: `--keyring=/builddir/new/gpgkey.asc --signature=/builddir/new/mpd-0.24.15.tar.xz.sig --data=/builddir/new/mpd-0.24.15.tar.xz`

Phase 1 reason: `sha1-cert`

## gpgkey.asc

- certificates: 0392335A78083894A4301C43236E8A58C6DB4512
- found via: hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 5581 → 5523 bytes

```diff
(no change in sq inspect summary)
```

