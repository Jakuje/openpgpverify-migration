# Keyring update from upstream for isync

**Status: still-fails**

Failing call: `--keyring=/builddir/new/isync.keyring --signature=/builddir/new/isync-1.5.1.tar.gz.asc --data=/builddir/new/isync-1.5.1.tar.gz`

Phase 1 reason: `expired`

## isync.keyring

- from: https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x63bfd037cad71e8dff3aea3ac17714f08d1bdbba
- certificates (unchanged): 63BFD037CAD71E8DFF3AEA3AC17714F08D1BDBBA
- size: 16174 → 16166 bytes

```
curl -fsSL -o isync.keyring https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x63bfd037cad71e8dff3aea3ac17714f08d1bdbba
```

```diff
(no change in sq inspect summary)
```

## Verification with the upstream keyring

```
$ sqv ... isync-1.5.1.tar.gz
Signing key on 63BFD037CAD71E8DFF3AEA3AC17714F08D1BDBBA is bad:
           The primary key is not live
  because: Expired on 2022-05-22T16:31:18Z
rc=1
```

