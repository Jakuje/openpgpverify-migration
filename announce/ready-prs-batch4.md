# PRs ready to open

Generated 2026-10-26T14:23Z by `scripts/ready_list.py` from `/tmp/claude-1000/-home-jjelen-devel/d7f35f6e-ac0c-4840-8252-b22d83166897/scratchpad/batch4.txt`. Every package below passed Phase 1 (`%prep` with `%gpgverify` and `%openpgpverify` in mock, all verification calls logged), has no open PR, and its rawhide branch is still at the tested commit (checked when this list was generated).

## Ready (14)

| Package | Maintainers | Diff | Release bump | `%{?rhel}` | BR gnupg2 | Tested |
|---|---|---|---|---|---|---|
| [asahi-installer](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/asahi-installer/) | dcavalca | +2/-1 |  |  | kept | 2026-10-26 |
| [budgie-backgrounds](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/budgie-backgrounds/) | joshstrobl | +6/-3 | yes |  | dropped (checked) | 2026-10-26 |
| [clang15](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/clang15/) | frantisekz tuliom | +7/-3 | yes |  | kept | 2026-10-26 |
| [feather](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/feather/) | js | +2/-1 |  |  | kept | 2026-10-26 |
| [forgejo](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/forgejo/) | nphilipp-rh nphilipp | +2/-1 |  |  | kept | 2026-10-26 |
| [freeipa](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/freeipa/) | abbra twoerner dhanina rcritten simo | +6/-2 | yes |  | kept | 2026-10-26 |
| [gcompris-qt](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/gcompris-qt/) | musuruan | +6/-2 | yes |  |  | 2026-10-26 |
| [grout](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/grout/) | rjarry mruprich | +2/-2 |  |  | dropped (checked) | 2026-10-26 |
| [kitty](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/kitty/) | jonathanspw zawertun solopasha atim | +2/-2 |  |  | dropped (checked) | 2026-10-26 |
| [libclc22](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/libclc22/) | kkleine | +6/-2 | yes |  | kept | 2026-10-26 |
| [llvm15](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/llvm15/) | frantisekz tuliom | +7/-3 | yes |  | kept | 2026-10-26 |
| [llvm19](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/llvm19/) | carlwgeorge nikic rcallicotte mikedep333 | +7/-3 | yes |  | kept | 2026-10-26 |
| [llvm21](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/llvm21/) | tuliom | +3/-2 |  |  | kept | 2026-10-26 |
| [passwordsafe](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/passwordsafe/) | carllibpst | +2/-2 |  |  |  | 2026-10-26 |

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
