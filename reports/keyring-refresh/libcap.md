# Keyring refresh for libcap

**Status: still-fails**

Failing call: `--keyring=/builddir/new/29EE848AE2CCF3F4.asc --signature=/builddir/new/libcap-2.78.tar.sign --data=-`

Phase 1 reason: `sha1-cert`

## 29EE848AE2CCF3F4.asc

- certificates: 38A644698C69787344E954CE29EE848AE2CCF3F4
- found via: hkps://keys.openpgp.org, hkps://keyserver.ubuntu.com, hkps://sks.pod01.fleetstreetops.com
- size: 6479 → 9516 bytes

Commands (run in a copy of dist-git):

```
sq --home=none network keyserver search 38A644698C69787344E954CE29EE848AE2CCF3F4 --output 29EE848AE2CCF3F4.asc --overwrite
```

```diff
--- dist-git/29EE848AE2CCF3F4.asc
+++ refreshed/29EE848AE2CCF3F4.asc
@@ -10,6 +10,6 @@
            UserID: Andrew G. Morgan <morgan@kernel.org>
                    Invalid: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
                    because: SHA1 is not considered secure
-self-signatures PositiveCertification: 2011-10-12, 2011-10-15
+self-signatures PositiveCertification: 2011-10-07, 2011-10-12, 2011-10-15
 self-signatures SubkeyBinding: 2011-10-07
-third-party GenericCertification: 2
+third-party GenericCertification: 5
```

## Verification with the refreshed keyring

```
$ zcat libcap-2.78.tar.gz | sqv ... -
Signing key on 38A644698C69787344E954CE29EE848AE2CCF3F4 is not bound:
           No binding signature at time 2026-04-05T18:09:50Z
  because: Policy rejected non-revocation signature (PositiveCertification) requiring second pre-image resistance
  because: SHA1 is not considered secure
rc=1
```

