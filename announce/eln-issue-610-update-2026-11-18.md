Update on the ELN packages that verify sources with `%gpgverify` or gpg (state as of 2026-11-18):

| | Packages (of 164) |
|---|---|
| Converted to `%openpgpverify` in rawhide | 101 |
| PR open | 32 |
| Still to do | 29 |
| Signature check dropped by the maintainer (teckit, xkeyboard-config) | 2 |

**Open PRs** (32), waiting for the maintainers: aide#16, autoconf-archive#8, bind#65, bzip2#10, coreutils#24, dhcpcd#29, expat#8, gpgme#26, ldns#10, libdisplay-info#1, libguestfs#12, libmnl#4, libnetfilter_conntrack#4, libssh2#4, libtasn1#8, libtpms#5, libxcrypt#23, llvm22#3, lttng-ust#3, mdadm#14, mkfontscale#2, nettle#17, nmstate#153, pdfio#5, poppler#7, pyparted#5, samba#46, sssd#94, time#7, usbredir#3, wayland#10, xterm#5. From around 23 Nov I plan to ask a proven packager to merge the ones without a response.

**Still to do** (29):

- 3 with a PR prepared that updates the keyring (the current one holds old v3 keys that sqv cannot read), not opened yet: apache-commons-net, e2fsprogs, httpd
- 26 where no working key is published, so the upstream (or the maintainer) has to act. Each has a bug on [rhbz#2569052](https://bugzilla.redhat.com/show_bug.cgi?id=2569052) explaining the options:
  - DSA-1024 key (16): Xaw3d, bash, bison, cpio, dns-root-data, file, irssi, libXpm, libburn, libdvdnav, libdvdread, libisoburn, libisofs, libmpc, nghttp2, nmap
  - SHA-1 self-signatures on the key (10): cyrus-imapd, dos2unix, ed, findutils, git, libcap, libvoikko, rust, s-nail, voikko-fi

These 26 can't move to `%openpgpverify` until their upstream key changes; I'm following up on the bugs.

Details:

- Progress report with per-package status: https://github.com/Jakuje/openpgpverify-migration/blob/main/reports/progress-2026-11-18.md
- Patches and PR texts: https://github.com/Jakuje/openpgpverify-migration/tree/main/proposals
- Change tracker: [rhbz#2523619](https://bugzilla.redhat.com/show_bug.cgi?id=2523619)
