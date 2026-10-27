# Keyrings fixed by the key URL in the spec

Generated 2026-10-27 by `scripts/refresh_keys.py propose-upstream` for all 254 packages whose `%openpgpverify` check fails.
For each failing keyring it takes the URL the spec gives (the `Source:` URL or a URL in the comment above it), downloads it with `curl` and keeps it only if it holds exactly the same certificate fingerprints as the file in dist-git and differs from it. Then sqv runs with that file, unchanged, on the release in the lookaside cache. No keyserver merging, no spec change: the PR just replaces the keyring with the current upstream copy.

## Upstream copy verifies the release (22)

| Package | ELN | URL | Host sqv | Review |
|---|---|---|---|---|
| cgit |  | https://www.zx2c4.com/keys/AB9942E6D4A4CFC3412620A749FC7012A5DE03AE.asc | skipped (stdin data; Phase 1 checks) | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/cgit.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/cgit/) |
| dhcpdump |  | https://raw.githubusercontent.com/bbonev/dhcpdump/v2.00/debian/upstream/signing-key.asc | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/dhcpdump.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/dhcpdump/) |
| drm_info |  | https://emersion.fr/.well-known/openpgpkey/hu/dj3498u4hyyarh35rkjfnghbjxug6b19 | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/drm_info.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/drm_info/) |
| expat | yes | https://keys.openpgp.org/vks/v1/by-fingerprint/3176EF7DB2367F1FCA4F306B1F9B0E909AF37285 | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/expat.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/expat/) |
| keepassxc |  | https://keepassxc.org/keepassxc_master_signing_key.asc | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/keepassxc.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/keepassxc/) |
| knot-resolver |  | https://secure.nic.cz/files/knot-resolver/kresd-keyblock.asc | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/knot-resolver.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/knot-resolver/) |
| libidn2 | yes | https://keys.openpgp.org/vks/v1/by-fingerprint/B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/libidn2.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/libidn2/) |
| mingw-libidn2 |  | https://keys.openpgp.org/vks/v1/by-fingerprint/B1D2BD1375BECB784CF4F8C4D73CF638C53C06BE | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/mingw-libidn2.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/mingw-libidn2/) |
| opam |  | https://opam.ocaml.org/opam-dev-pubkey.pgp | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/opam.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/opam/) |
| openresolv |  | http://keyserver.ubuntu.com/pks/lookup?op=get&search=0xa785ed2755955d9e93ea59f6597f97ea9ad45549 | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/openresolv.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/openresolv/) |
| p11-kit | yes | https://p11-glue.github.io/p11-glue/p11-kit/p11-kit-release-keyring.gpg | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/p11-kit.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/p11-kit/) |
| poppler | yes | https://pgp.surfnet.nl/pks/lookup?op=get&search=0xCA262C6C83DE4D2FB28A332A3A6A4DB839EAA6D7 | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/poppler.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/poppler/) |
| quodlibet |  | https://keys.openpgp.org/vks/v1/by-fingerprint/E0AA0F031DBD80FFBA57B06D5A62D0CAB6264964 | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/quodlibet.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/quodlibet/) |
| rpki-client |  | https://keys.openpgp.org/vks/v1/by-fingerprint/B5B6416FEA6DDA05EA562A9FCB987F2783972FF9 | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/rpki-client.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/rpki-client/) |
| sway |  | https://emersion.fr/.well-known/openpgpkey/hu/dj3498u4hyyarh35rkjfnghbjxug6b19 | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/sway.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/sway/) |
| swaybg |  | https://keys.openpgp.org/vks/v1/by-fingerprint/34FF9526CFEF0E97A340E2E40FDE7BE0E88F5E48 | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/swaybg.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/swaybg/) |
| weechat |  | https://keys.openpgp.org/vks/v1/by-fingerprint/A9AB5AB778FA5C3522FD0378F82F4B16DEC408F8 | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/weechat.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/weechat/) |
| wlroots |  | https://emersion.fr/.well-known/openpgpkey/hu/dj3498u4hyyarh35rkjfnghbjxug6b19 | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/wlroots.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/wlroots/) |
| xdg-desktop-portal-wlr |  | https://emersion.fr/.well-known/openpgpkey/hu/dj3498u4hyyarh35rkjfnghbjxug6b19 | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/xdg-desktop-portal-wlr.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/xdg-desktop-portal-wlr/) |
| xterm | yes | https://invisible-island.net/public/dickey@invisible-island.net-rsa3072.asc | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/xterm.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/xterm/) |
| xz | yes | https://tukaani.org/misc/lasse_collin_pubkey.txt | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/xz.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/xz/) |
| yascreen |  | https://raw.githubusercontent.com/bbonev/yascreen/master/debian/upstream/signing-key.asc | pass | [review](https://github.com/Jakuje/openpgpverify-migration/tree/main/reports/keyring-upstream/yascreen.md) · [draft](https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals/yascreen/) |

To turn these into tested PRs (the approval is bound to the exact file, as for keyserver refreshes):

```
for p in cgit dhcpdump drm_info expat keepassxc knot-resolver libidn2 mingw-libidn2 opam openresolv p11-kit poppler quodlibet rpki-client sway swaybg weechat wlroots xdg-desktop-portal-wlr xterm xz yascreen; do
    scripts/refresh_keys.py approve $p --note "upstream URL copy"
done
scripts/phase1.py --jobs 1 --prune-sources --inventory data/inventory/inventory-2026-10-27.jsonl cgit dhcpdump drm_info expat keepassxc knot-resolver libidn2 mingw-libidn2 opam openresolv p11-kit poppler quodlibet rpki-client sway swaybg weechat wlroots xdg-desktop-portal-wlr xterm xz yascreen
scripts/render_proposals.py --list data/proposal-list.txt
```

## Upstream copy has the same key but still fails (32)

Upstream has a newer copy of the key, but sqv still rejects the release with it (typically: the new self-signatures are newer than the release signature, or still SHA-1). Good bug candidates: the maintainer or upstream has to act (re-sign, or a new release).

cyrus-imapd, dialog, dns-root-data, dnssec-trigger, dos2unix, ed, eggdrop, ffmpeg, iec16022, isync, john, kanshi, libdisplay-info, libdvdnav, libdvdread, liblxi, libtpms, lxi-tools, mako, ncurses, nginx-mod-fancyindex, normalize, psad, s-nail, signify, skribilo, slurp, spamassassin, swayidle, tio, wlr-randr, wlroots0.19

## Different certificates at the URL (9)

The file at the URL no longer has the same set of keys (e.g. an Apache `KEYS` file or the GNU keyring gained or lost members). Switching to it adds or removes trusted keys, so that is a maintainer call.

apache-commons-vfs, bison, e2fsprogs, guile-gnutls, libredwg, maven-reporting-api, maven-reporting-impl, ntpsec, opendoas

