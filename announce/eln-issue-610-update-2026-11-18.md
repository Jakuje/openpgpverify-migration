Status of the 164 ELN packages that verified sources with `%gpgverify` or GnuPG (as of 2026-11-18):

| | Packages |
|---|---|
| Converted to `%openpgpverify` in rawhide | 101 |
| PR open, waiting for the maintainer | 32 |
| PR prepared, not opened yet | 3 |
| Blocked on the upstream key (bug filed) | 26 |
| Signature check dropped by the maintainer | 2 |

The 26 blocked packages have no published key that sqv accepts: 16 use a DSA-1024 key, 10 have SHA-1 self-signatures on the key. They need a new or re-signed key from upstream; I'm following up on the bugs. From around 23 Nov I plan to ask a proven packager to merge the open PRs that get no response.

Per-package details, with the PRs and bugs: https://github.com/Jakuje/openpgpverify-migration/blob/main/reports/eln-2026-11-18.md
