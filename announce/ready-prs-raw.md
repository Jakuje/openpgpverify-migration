# PRs ready to open

Generated 2026-10-26T20:26Z by `scripts/ready_list.py` from `/tmp/claude-1000/-home-jjelen-devel/d7f35f6e-ac0c-4840-8252-b22d83166897/scratchpad/raw32.lst`. Every package below passed Phase 1 (`%prep` with `%gpgverify` and `%openpgpverify` in mock, all verification calls logged), has no open PR, and its rawhide branch is still at the tested commit (checked when this list was generated).

These specs called GnuPG directly (`gpgv`, `gpgv2` or `gpg2`, some through a temporary keyring or GNUPGHOME), not `%gpgverify`. The PRs replace that with one `%openpgpverify` call; the old runs used the original GnuPG commands. knot, gpgme, nmstate and pam_mount were rewritten by hand (`manual/PKG.patch`), the others by `scripts/convert.py` (`rewrite_raw`). Please read these diffs a bit more carefully than the usual rename.

## Ready (7)

| Package | Maintainers | Diff | Release bump | `%{?rhel}` | BR gnupg2 | Tested |
|---|---|---|---|---|---|---|
| [dd_rescue](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/dd_rescue/) | rebus ndim jussilehtola steve | +2/-2 |  |  | dropped (checked) | 2026-10-26 |
| [gpgme](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/gpgme/) | jkucera mhlavink mrc0mmand | +6/-3 | yes |  | kept | 2026-10-26 |
| [gsi-openssh](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/gsi-openssh/) | ellert | +6/-3 | yes |  | dropped (checked) | 2026-10-26 |
| [knot](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/knot/) | pwouters jruzicka | +6/-7 | yes |  | dropped (checked) | 2026-10-26 |
| [nmstate](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/nmstate/) | cathay4t josie ffmancera jvaclav ihuguet rrajesh till praksany | +2/-4 |  |  | dropped (checked) | 2026-10-26 |
| [pam_mount](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/pam_mount/) | aflyhorse steve | +7/-5 | yes |  | dropped (checked) | 2026-10-26 |
| [tpm2-openssl](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/tpm2-openssl/) | afreof dbelyavs | +6/-3 | yes |  | dropped (checked) | 2026-10-26 |

## Opening a PR

The patch is the complete commit (author, message with the `Assisted-by:` trailer); `PR.md` has the title and description.

```sh
P=libmnl   # package
fedpkg clone "$P" && cd "$P"
git am ~/devel/openpgpverify-migration/proposals/"$P"/0001-*.patch
fedpkg fork                      # adds a remote named after your FAS user
git push "$USER" HEAD:openpgpverify
# then open the PR from the fork (branch openpgpverify -> rawhide) in the web UI,
# pasting title and description from proposals/$P/PR.md
```
