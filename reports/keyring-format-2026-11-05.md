# Keyrings sqv cannot read (2026-11-05)

Phase 1 reasons `unparseable-cert` and `concatenated-armor`. sqv stops at the
first certificate it cannot parse ("Malformed certificate in keyring ...
unknown version"), so one old key in a multi-key file fails the whole keyring.
Tested against the current release signature, with the signer's key as found:

| Package | ELN | Filtered copy of dist-git keyring (gpg import/export) | keys.openpgp.org | keyserver.ubuntu.com | Outcome |
|---|---|---|---|---|---|
| ant-antunit | | verifies | verifies | verifies | fixable |
| apache-commons-net | | verifies | fails (binding) | verifies | fixable |
| apache-commons-text | | verifies | fails (binding) | verifies | fixable |
| httpd | yes | verifies | fails (binding) | verifies | fixable |
| libextractor | | verifies | fails (SHA-1) | verifies | fixable |
| e2fsprogs | yes | fails (expired subkey) | verifies | verifies | fixable |
| gnucobol | | fails (expired) | verifies | verifies | fixable |
| tor | | fails (expired) | verifies | fails (expired) | fixable (keyring was readable; reason mislabelled) |
| apache-commons-vfs | | fails (SHA-1) | fails (SHA-1) | fails (SHA-1) | bug |
| findutils | | fails (SHA-1) | not found | fails (SHA-1) | bug |

Decision 2026-11-05: packages with a multi-key file (ant-antunit,
apache-commons-net, apache-commons-text, httpd, libextractor, gnucobol) get a
bug, and the maintainer decides how to fix the keyring. No PRs for these.
