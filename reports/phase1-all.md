# Phase 1 results

Generated 2026-10-26T20:27Z from `data/state/packages.jsonl`: 577 of 595 packages tested.

| Status | Packages |
|---|---|
| `tested` | 276 |
| `regression` | 254 |
| `superseded` | 41 |
| `guard-failed` | 2 |
| `not-buildable` | 2 |
| `skipped` | 2 |

| Regression reason | Calls |
|---|---|
| `sha1-cert` | 116 |
| `expired` | 75 |
| `sha1-sig` | 38 |
| `weak-key` | 13 |
| `unparseable-cert` | 11 |
| `v3-sig` | 8 |
| `keybox` | 5 |
| `binding-after-signature` | 4 |
| `concatenated-armor` | 1 |

| Package | Status | Calls old→new | Chroots | Notes |
|---|---|---|---|---|
| 0install | `tested` | 1→1 | rawhide: both-pass |  |
| AusweisApp2 | `tested` | 1→1 | rawhide: both-pass |  |
| BibTool | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| ImageMagick | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| NetworkManager-strongswan | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires: gnupg2 |
| SDL3 | `tested` | 1→1 | rawhide: both-pass, eln: both-pass |  |
| SDL3_net | `tested` | 1→1 | rawhide: both-pass |  |
| Xaw3d | `regression` | 1→1 | rawhide: regression | reason: weak-key |
| abcde | `tested` | 1→1 | rawhide: both-pass |  |
| acl | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| aesfix | `regression` | 1→1 | rawhide: regression | reason: v3-sig |
| aeskeyfind | `regression` | 1→1 | rawhide: regression | reason: v3-sig |
| aide | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| anet | `tested` | 1→1 | rawhide: both-pass |  |
| ansible-collection-dellemc-openmanage | `tested` | 1→1 | rawhide: both-pass |  |
| ansifilter | `tested` | 1→1 | rawhide: both-pass |  |
| ant-antunit | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: unparseable-cert |
| anymeal | `tested` | 1→1 | rawhide: both-pass |  |
| apache-commons-net | `regression` | 1→1 | rawhide: regression | reason: unparseable-cert |
| apache-commons-text | `regression` | 1→1 | rawhide: regression | reason: unparseable-cert |
| apache-commons-vfs | `regression` | 1→1 | rawhide: regression | reason: unparseable-cert |
| apachetop | `tested` | 1→1 | rawhide: both-pass |  |
| asahi-installer | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| asterisk | `regression` | 1→1 | rawhide: regression | reason: keybox; keyring refresh: proposed |
| attr | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| autoconf-archive | `tested` | 1→1 | rawhide: both-pass |  |
| b43-fwcutter | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| babeltrace | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| babeltrace2 | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| basez | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| bash | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-sig |
| batctl | `tested` | 1→1 | rawhide: both-pass |  |
| bc | `tested` | 1→1 | rawhide: both-pass |  |
| bcachefs-tools | `tested` | 1→1 | rawhide: both-pass |  |
| bemenu | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| bind | `guard-failed` | 0→0 | rawhide: guard-failed, eln: not-verified | old spec executed no gpgverify call (prep rc 0); the unchanged spec does not verify sources in this chroot; B… |
| bind9-next | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  gpgverify |
| bino | `tested` | 1→1 | rawhide: both-pass |  |
| bison | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-sig |
| blktrace | `tested` | 1→1 | rawhide: both-pass |  |
| bmake | `regression` | 1→1 | rawhide: regression | dropped conditional BR: BuildRequires: gnupg2; reason: sha1-cert; keyring refresh: still-fails |
| borgbackup | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| botan3 | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| bpfmon | `tested` | 1→1 | rawhide: both-pass |  |
| browserpass | `tested` | 1→1 | rawhide: both-pass |  |
| btrfs-progs | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| budgie-backgrounds | `tested` | 1→1 | rawhide: both-pass |  |
| budgie-desktop | `tested` | 1→1 | rawhide: both-pass |  |
| budgie-desktop-defaults | `tested` | 1→1 | rawhide: both-pass |  |
| bzip2 | `tested` | 1→1 | rawhide: both-pass |  |
| cage | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| cairomm1.16 | `superseded` | -→- |  |  |
| cgit | `regression` | 2→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| checkpolicy | `superseded` | -→- |  |  |
| chewing-editor | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| chrony | `tested` | 1→1 | rawhide: both-pass, eln: both-pass | BR gnupg2 kept (review) |
| cksfv | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| clang15 | `tested` | 1→1 | rawhide: both-pass |  |
| clang18 | `regression` | 2→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| cmocka | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| compat-gpgme124 | `tested` | 1→1 | rawhide: both-pass |  |
| conflict | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| conntrack-tools | `tested` | 1→1 | rawhide: both-pass |  |
| conserver | `tested` | 1→1 | rawhide: both-pass |  |
| coreutils | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| courier-unicode | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| cpio | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-sig |
| cproto | `tested` | 1→1 | rawhide: both-pass |  |
| crun | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| cryptlib | `regression` | 2→1 | rawhide: regression | reason: sha1-cert; keyring refresh: not-found |
| cryptobone | `regression` | 2→1 | rawhide: regression | reason: sha1-cert; keyring refresh: not-found |
| cryptopp | `tested` | 1→1 | rawhide: both-pass |  |
| cscppc | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| csdiff | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| csmock | `tested` | 1→1 | rawhide: both-pass |  |
| cswrap | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| ctstream | `superseded` | 1→1 | rawhide: both-pass |  |
| curl | `not-buildable` | 0→0 | rawhide: not-buildable, eln: not-buildable | unchanged spec: installdeps failed; unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| cvs | `regression` | 1→1 | rawhide: regression | reason: v3-sig |
| cyrus-imapd | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| davfs2 | `tested` | 1→1 | rawhide: both-pass |  |
| dbus | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| dbus-glib | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| dbus-python | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| dd_rescue | `tested` | 1→1 | rawhide: both-pass |  |
| debugedit | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: keybox |
| dehydrated | `tested` | 1→1 | rawhide: both-pass |  |
| dhcp | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| dhcpcd | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: sha1-cert; reason: sha1-cert; keyring refresh: proposed |
| dhcpdump | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| dialog | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| dino | `tested` | 1→1 | rawhide: both-pass |  |
| diskimage-builder | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires: /usr/bin/gpgv2 |
| disorderfs | `tested` | 1→1 | rawhide: both-pass |  |
| dnf | `tested` | 1→1 | rawhide: both-pass, eln: both-pass | BR gnupg2 kept (review) |
| dns-root-data | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| dnssec-trigger | `regression` | 1→1 | rawhide: regression | dropped conditional BR: BuildRequires: gnupg2; reason: sha1-sig |
| dos2unix | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| dotnet10.0 | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| drm_info | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| dropbear | `tested` | 1→1 | rawhide: both-pass |  |
| e2fsprogs | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: unparseable-cert; reason: unparseable-cert |
| ed | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: sha1-sig; reason: sha1-sig |
| eggdrop | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| electron-cash | `regression` | 1→1 | rawhide: regression | reason: weak-key |
| electrum | `tested` | 1→1 | rawhide: both-pass |  |
| emacs | `superseded` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| ethtool | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| exim | `tested` | 1→1 | rawhide: both-pass |  |
| expat | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| facter | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| fail2ban | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| fapolicyd | `superseded` | 2→2 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; replaced conditional BR in place: BuildRequires: gpgverify; rhel conditio… |
| fcft | `tested` | 1→1 | rawhide: both-pass |  |
| fcitx5 | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| fcitx5-anthy | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| fcitx5-chewing | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| fcitx5-chinese-addons | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| fcitx5-configtool | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| fcitx5-gtk | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| fcitx5-hangul | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| fcitx5-kkc | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| fcitx5-libthai | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| fcitx5-lua | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| fcitx5-m17n | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| fcitx5-qt | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| fcitx5-rime | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| fcitx5-sayura | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| fcitx5-skk | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| fcitx5-table-extra | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| fcitx5-table-other | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| fcitx5-unikey | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| fcitx5-zhuyin | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| feather | `tested` | 1→1 | rawhide: both-pass |  |
| fedrq | `tested` | 1→1 | rawhide: both-pass |  |
| ffmpeg | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| file | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: sha1-sig; reason: sha1-sig |
| findutils | `regression` | 1→1 | rawhide: regression | reason: unparseable-cert |
| fio | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed |
| fips-provider | `superseded` | 1→1 | rawhide: both-pass, eln: both-pass | BR gnupg2 kept (review) |
| fish | `tested` | 1→1 | rawhide: both-pass |  |
| flashrom | `regression` | 1→1 | rawhide: regression | reason: weak-key |
| foot | `tested` | 1→1 | rawhide: both-pass |  |
| fop | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| forgejo | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| freeipa | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| freetalk | `tested` | 1→1 | rawhide: both-pass |  |
| fuse-encfs | `skipped` | -→- |  |  |
| fuse-sshfs | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| gcl | `tested` | 1→1 | rawhide: both-pass |  |
| gcompris-qt | `tested` | 1→1 | rawhide: both-pass |  |
| geeqie | `superseded` | -→- |  |  |
| gencolormap | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| getdns | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| git | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: sha1-cert; reason: sha1-cert; keyring refresh: proposed |
| glinf | `regression` | 1→1 | rawhide: regression | reason: binding-after-signature; keyring refresh: still-fails |
| glpk | `regression` | 1→1 | rawhide: regression | reason: v3-sig |
| gnuastro | `tested` | 1→1 | rawhide: both-pass |  |
| gnucobol | `regression` | 1→1 | rawhide: regression | reason: unparseable-cert |
| gnulib-l10n | `tested` | 1→1 | rawhide: both-pass |  |
| gnupg2 | `superseded` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| gnutls | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| gpgme | `tested` | 2→1 | rawhide: both-pass |  |
| gpgmepp | `tested` | 1→1 | rawhide: both-pass |  |
| gplugin | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| grep | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| grim | `superseded` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| grout | `tested` | 1→1 | rawhide: both-pass |  |
| growlight | `tested` | 1→1 | rawhide: both-pass |  |
| gscan2pdf | `superseded` | -→- |  |  |
| gsi-openssh | `tested` | 1→1 | rawhide: both-pass |  |
| gsl | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| guestfs-tools | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| guile-gnutls | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| haruna | `tested` | 1→1 | rawhide: both-pass |  |
| haunt | `tested` | 1→1 | rawhide: both-pass |  |
| hcxtools | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| hello | `tested` | 1→1 | rawhide: both-pass |  |
| hiera | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| hivex | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: sha1-cert; reason: sha1-cert; keyring refresh: still-fails |
| httpd | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: unparseable-cert; reason: unparseable-cert |
| hxtools | `regression` | 1→1 | rawhide: regression | reason: sha1-sig; keyring refresh: proposed |
| i3 | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| i3lock | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| i3status | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| ibus-chewing | `superseded` | 1→1 | rawhide: both-pass |  |
| iec16022 | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| indent | `superseded` | -→- |  |  |
| inkscape | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: weak-key |
| inn | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| iotop-c | `superseded` | 1→1 | rawhide: both-pass |  |
| ipcalc | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| iptables | `tested` | 1→1 | rawhide: both-pass, eln: both-pass |  |
| irssi | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; reason: sha1-sig |
| isync | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: still-fails |
| jalv | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| jigdo | `tested` | 1→1 | rawhide: both-pass |  |
| john | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| kanshi | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| kdsoap | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| kea | `superseded` | -→- |  |  |
| keepass | `tested` | 1→1 | rawhide: both-pass |  |
| keepassxc | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| kio-fuse | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| kitty | `tested` | 1→1 | rawhide: both-pass |  |
| knot | `tested` | 2→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:	gnupg2 |
| knot-resolver | `regression` | 2→1 | rawhide: regression | dropped conditional BR: BuildRequires:  gnupg2; reason: expired; keyring refresh: proposed |
| kronometer | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| kuserfeedback | `tested` | 1→1 | rawhide: both-pass |  |
| kvantum | `tested` | 1→1 | rawhide: both-pass |  |
| ldns | `tested` | 1→1 | rawhide: both-pass |  |
| libHX | `regression` | 1→1 | rawhide: regression | reason: sha1-sig; keyring refresh: proposed |
| libXpm | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-sig |
| libbsd | `tested` | 1→1 | rawhide: both-pass |  |
| libburn | `regression` | 1→1 | rawhide: regression, eln: regression | reason: sha1-sig; reason: sha1-sig |
| libcap | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| libchewing | `superseded` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libchipcard | `tested` | 1→1 | rawhide: both-pass |  |
| libclc22 | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libdisplay-info | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| libdnf | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| libdvdnav | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| libdvdread | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| libeatmydata | `tested` | 1→1 | rawhide: both-pass |  |
| libextractor | `regression` | 1→1 | rawhide: regression | reason: unparseable-cert |
| libgnt | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libgpg-error | `superseded` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libgsasl | `regression` | 1→1 | rawhide: regression | reason: binding-after-signature; keyring refresh: proposed |
| libguestfs | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| libidn2 | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| libime | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| libisds | `superseded` | -→- |  |  |
| libisoburn | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: sha1-sig; reason: sha1-sig |
| libisofs | `regression` | 1→1 | rawhide: regression, eln: regression | reason: sha1-sig; reason: sha1-sig |
| libksba | `superseded` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| liblxi | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| libmd | `tested` | 1→1 | rawhide: both-pass |  |
| libmnl | `tested` | 1→1 | rawhide: both-pass |  |
| libmodsecurity | `tested` | 1→1 | rawhide: both-pass |  |
| libmodulemd | `superseded` | 1→1 | rawhide: both-pass, eln: both-pass | BR gnupg2 kept (review) |
| libmpc | `regression` | 1→1 | rawhide: regression | reason: weak-key |
| libnbd | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| libnetfilter_conntrack | `tested` | 1→1 | rawhide: both-pass |  |
| libnftnl | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libnice | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| libnids | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| libptytty | `tested` | 1→1 | rawhide: both-pass |  |
| libredwg | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| libreswan | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| librhsm | `tested` | 1→1 | rawhide: both-pass |  |
| libselinux | `superseded` | -→- |  |  |
| libsemanage | `superseded` | -→- |  |  |
| libssh | `superseded` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libssh2 | `tested` | 1→1 | rawhide: both-pass, eln: both-pass | BR gnupg2 kept (review) |
| libstrophe | `tested` | 1→1 | rawhide: both-pass |  |
| libtalloc | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| libtasn1 | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| libtdb | `regression` | 1→1 | rawhide: regression | reason: keybox; keyring refresh: proposed |
| libtevent | `regression` | 1→1 | rawhide: regression | reason: keybox; keyring refresh: proposed |
| libtpms | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| libusb1 | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libuv | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| libvoikko | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| libxcrypt | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| lilv | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| lld15 | `tested` | 1→1 | rawhide: both-pass |  |
| lld18 | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| llvm | `tested` | 2→2 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| llvm14 | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| llvm15 | `tested` | 2→2 | rawhide: both-pass | BR gnupg2 kept (review) |
| llvm18 | `regression` | 3→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| llvm19 | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| llvm20 | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| llvm21 | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| llvm22 | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| log4cplus | `superseded` | 1→1 | rawhide: both-pass |  |
| logrotate | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| loudmouth | `regression` | 1→1 | rawhide: regression | reason: sha1-sig; keyring refresh: still-fails |
| lttng-ust | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| lua-unbound | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| lxi-tools | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| lynx | `tested` | 1→1 | rawhide: both-pass, eln: both-pass |  |
| maildrop | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| mako | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| man-db | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| mat2 | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| maven-doxia | `tested` | 1→1 | rawhide: both-pass |  |
| maven-doxia-sitetools | `tested` | 1→1 | rawhide: both-pass |  |
| maven-reporting-api | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| maven-reporting-impl | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| mcstrans | `superseded` | -→- |  |  |
| mdadm | `tested` | 1→1 | rawhide: both-pass |  |
| mimedefang | `tested` | 1→1 | rawhide: both-pass |  |
| mingw-SDL3 | `tested` | 1→1 | rawhide: both-pass |  |
| mingw-cmocka | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| mingw-libidn2 | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| mingw-libssh2 | `tested` | 1→1 | rawhide: both-pass |  |
| mingw-nettle | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| mingw-objfw | `tested` | 1→1 | rawhide: both-pass |  |
| mingw-pcre | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| mingw-usbredir | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| mkfontscale | `tested` | 1→1 | rawhide: both-pass |  |
| mkvtoolnix | `tested` | 1→1 | rawhide: both-pass |  |
| mod_perl | `tested` | 1→1 | rawhide: both-pass |  |
| mooltipass-udev | `tested` | 1→1 | rawhide: both-pass |  |
| mpd | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| mpdscribble | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| mpop | `tested` | 1→1 | rawhide: both-pass |  |
| msmtp | `tested` | 1→1 | rawhide: both-pass |  |
| mucalc | `tested` | 1→1 | rawhide: both-pass |  |
| munge | `superseded` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| munin | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: still-fails |
| musl | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| nano | `tested` | 1→1 | rawhide: both-pass |  |
| nbdkit | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| ncmpc | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| ncurses | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; reason: expired; keyring refresh: proposed |
| nettle | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: still-fails |
| nettle3.10 | `tested` | 1→1 | rawhide: both-pass |  |
| newsboat | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| nftables | `tested` | 1→1 | rawhide: both-pass |  |
| nghttp2 | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: no-update |
| nghttp3 | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| nginx-mod-fancyindex | `regression` | 1→1 | rawhide: regression | reason: weak-key |
| ngtcp2 | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| nilfs-utils | `tested` | 1→1 | rawhide: both-pass |  |
| nmap | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| nmstate | `tested` | 2→1 | rawhide: both-pass |  |
| normalize | `regression` | 1→1 | rawhide: regression | reason: v3-sig |
| notcurses | `tested` | 1→1 | rawhide: both-pass |  |
| notmuch | `superseded` | -→- |  |  |
| npth | `superseded` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| nss-pem | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| nss_wrapper | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| ntpsec | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| oath-toolkit | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| objfw | `tested` | 1→1 | rawhide: both-pass |  |
| ocaml-augeas | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| ocaml-mysql | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| oclock | `regression` | 1→1 | rawhide: regression | reason: weak-key |
| ocserv | `regression` | 1→1 | rawhide: regression | dropped conditional BR: BuildRequires:	gnupg2; reason: sha1-cert; keyring refresh: proposed |
| oidentd | `tested` | 1→1 | rawhide: both-pass |  |
| opam | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: not-found |
| openbgpd | `tested` | 1→1 | rawhide: both-pass |  |
| openconnect | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| opendoas | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: still-fails |
| openresolv | `regression` | 1→1 | rawhide: regression, eln: regression | reason: sha1-cert; reason: sha1-cert; keyring refresh: proposed |
| openssh | `superseded` | 1→0 | rawhide: manual | raw verification baseline passes |
| openssl-pkcs11 | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| openvpn | `tested` | 1→1 | rawhide: both-pass |  |
| p11-kit | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| pam_mount | `tested` | 2→1 | rawhide: both-pass |  |
| pam_wrapper | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| paperkey | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| par2cmdline | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| parallel | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| pari | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| pari-elldata | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| pari-galdata | `regression` | 1→1 | rawhide: regression | reason: v3-sig |
| pari-galpol | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| pari-nflistdata | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| pari-nftables | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| pari-seadata | `regression` | 2→1 | rawhide: regression | reason: sha1-sig |
| parted | `superseded` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| pass-audit | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| passwordsafe | `tested` | 1→1 | rawhide: both-pass |  |
| pcre2 | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| pcsc-lite | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| pcsc-lite-ccid | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| pdfgrep | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: weak-key |
| pdfio | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| pdns-recursor | `tested` | 1→1 | rawhide: both-pass |  |
| perl-Net-DNS | `tested` | 1→1 | rawhide: both-pass |  |
| perl-WWW-OrangeHRM-Client | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: weak-key |
| php | `tested` | 1→1 | rawhide: both-pass, eln: both-pass | BR gnupg2 kept (review) |
| phpMyAdmin | `tested` | 1→1 | rawhide: both-pass |  |
| pianobar | `tested` | 1→1 | rawhide: both-pass |  |
| pinentry | `superseded` | 1→1 | rawhide: both-pass, eln: both-pass |  |
| pkcs11-provider | `superseded` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| poke | `tested` | 1→1 | rawhide: both-pass |  |
| policycoreutils | `superseded` | -→- |  |  |
| poppler | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: expired; reason: expired; keyring refresh: proposed |
| postfix-mta-sts-resolver | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| priv_wrapper | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| prosody | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: still-fails |
| psad | `regression` | 1→1 | rawhide: regression | reason: sha1-sig; keyring refresh: no-update |
| pspp | `tested` | 1→1 | rawhide: both-pass |  |
| puppet | `tested` | 1→1 | rawhide: both-pass |  |
| pv | `tested` | 1→1 | rawhide: both-pass |  |
| pylibacl | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| pyparted | `regression` | 1→1 | rawhide: regression | reason: keybox; keyring refresh: proposed |
| python-aodhclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-authres | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| python-automaton | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-b4 | `tested` | 1→1 | rawhide: both-pass |  |
| python-barbicanclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:    gpgverify |
| python-cinderclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-debtcollector | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-dijitso | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: no-update |
| python-ezgb | `tested` | 1→1 | rawhide: both-pass |  |
| python-futurist | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  gpgverify |
| python-glanceclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-gnocchiclient | `guard-failed` | 0→0 | rawhide: guard-failed | old spec executed no gpgverify call (prep rc 0); dropped conditional BR: BuildRequires:  /usr/bin/gpgv2; no u… |
| python-gnupg | `tested` | 1→1 | rawhide: both-pass | no unconditional BuildRequires; BR added before first section; BR gnupg2 kept (review) |
| python-hacking | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2; no unconditional BuildRequires; BR added before first… |
| python-heatclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-ironicclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-keystoneauth1 | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-keystoneclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-liblore | `tested` | 1→1 | rawhide: both-pass |  |
| python-libusb1 | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| python-magnumclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:    /usr/bin/gpgv2 |
| python-manilaclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-mistralclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-neutronclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-novaclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-octaviaclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-openstackclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-os-service-types | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  gpgverify |
| python-osc-lib | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-osc-placement | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:    /usr/bin/gpgv2 |
| python-oslo-concurrency | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-oslo-config | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  gpgverify; no unconditional BuildRequires; BR added before first sect… |
| python-oslo-context | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-oslo-i18n | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-oslo-log | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  %{gpgverify} |
| python-oslo-metrics | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-oslo-serialization | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-oslo-utils | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-oslotest | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-pass-import | `tested` | 1→1 | rawhide: both-pass |  |
| python-patatt | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| python-pskc | `tested` | 1→1 | rawhide: both-pass |  |
| python-reno | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-stevedore | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  gpgverify |
| python-sushy | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires: gpgverify |
| python-swiftclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-tackerclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-troveclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-zaqarclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-zstarfile | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| pyxattr | `superseded` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| qbittorrent | `tested` | 1→1 | rawhide: both-pass |  |
| qemu | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| qemu-sanity-check | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| qgpgme | `tested` | 1→1 | rawhide: both-pass |  |
| quodlibet | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| qvr | `tested` | 1→1 | rawhide: both-pass |  |
| rabbitmq-server | `tested` | 1→1 | rawhide: both-pass |  |
| radsecproxy | `tested` | 1→1 | rawhide: both-pass |  |
| radvd | `superseded` | -→- |  |  |
| recutils | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| redwax-tool | `tested` | 1→1 | rawhide: both-pass |  |
| remind | `tested` | 1→1 | rawhide: both-pass |  |
| reprotest | `tested` | 1→1 | rawhide: both-pass |  |
| resolv_wrapper | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| rhythmbox-alternative-toolbar | `tested` | 1→1 | rawhide: both-pass |  |
| river | `tested` | 1→1 | rawhide: both-pass |  |
| river-classic | `tested` | 1→1 | rawhide: both-pass |  |
| rkward | `tested` | 1→1 | rawhide: both-pass |  |
| rnp | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: not-found |
| roundcubemail | `tested` | 1→1 | rawhide: both-pass |  |
| rpki-client | `regression` | 1→1 | rawhide: regression | dropped conditional BR: BuildRequires:  gnupg2; reason: expired; keyring refresh: proposed |
| rpminspect | `tested` | 1→1 | rawhide: both-pass |  |
| rpminspect-data-centos | `tested` | 1→1 | rawhide: both-pass |  |
| rsakeyfind | `regression` | 1→1 | rawhide: regression | reason: v3-sig |
| rush | `tested` | 1→1 | rawhide: both-pass |  |
| rust | `regression` | 1→1 | rawhide: regression, eln: regression | dropped conditional BR: BuildRequires:  gpgverify; BR gnupg2 kept (review); reason: sha1-cert; reason: sha1-c… |
| rxvt-unicode | `tested` | 1→1 | rawhide: both-pass |  |
| s-nail | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| samba | `regression` | 2→1 | rawhide: regression | BR gnupg2 kept (keep); reason: expired; keyring refresh: proposed |
| screenkey | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| secilc | `superseded` | 1→1 | rawhide: both-pass |  |
| serd | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| setxkbmap | `tested` | 1→1 | rawhide: both-pass |  |
| shigofumi | `tested` | 1→1 | rawhide: both-pass |  |
| signify | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: weak-key |
| skribilo | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| slrn | `regression` | 1→1 | rawhide: regression | reason: v3-sig; keyring refresh: still-fails |
| slurp | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| sngrep | `tested` | 1→1 | rawhide: both-pass |  |
| socket_wrapper | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| sord | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| spamassassin | `regression` | 2→2 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| spread-sheet-widget | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: still-fails |
| squid | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| sratom | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| ssh-audit | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| sssd | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires: gpgverify |
| strongswan | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| stunnel | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: sha1-cert; reason: sha1-cert; keyring refresh: still-fails |
| suil | `tested` | 1→1 | rawhide: both-pass |  |
| supermin | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| swappy | `tested` | 1→1 | rawhide: both-pass |  |
| sway | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| swaybg | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| swayidle | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| swaylock | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| sysconftool | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| teckit | `skipped` | 0→0 | rawhide: guard-failed | old spec executed no gpgverify call (prep rc 0) |
| terminator | `tested` | 1→1 | rawhide: both-pass |  |
| tftp | `superseded` | -→- |  |  |
| time | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: binding-after-signature; keyring refresh: proposed |
| tinygo | `not-buildable` | 0→0 | rawhide: not-buildable | unchanged spec: installdeps failed |
| tio | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| tlf | `regression` | 1→1 | rawhide: regression | reason: weak-key |
| tmispell-voikko | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| tnftp | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| tomcat | `tested` | 1→1 | rawhide: both-pass |  |
| tomcli | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| tor | `regression` | 1→1 | rawhide: regression | reason: concatenated-armor |
| tpm2-openssl | `tested` | 1→1 | rawhide: both-pass |  |
| trader | `tested` | 1→1 | rawhide: both-pass |  |
| trafficserver | `tested` | 1→1 | rawhide: both-pass |  |
| trojan | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| tth | `tested` | 1→1 | rawhide: both-pass |  |
| uid_wrapper | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| unbound | `tested` | 1→1 | rawhide: both-pass, eln: both-pass | BR gnupg2 kept (review) |
| unrealircd | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| unrtf | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| usbredir | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| vali | `tested` | 1→1 | rawhide: both-pass |  |
| vim-latex | `tested` | 1→1 | rawhide: both-pass |  |
| virt-p2v | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| virt-top | `regression` | 1→1 | rawhide: regression, eln: regression | reason: sha1-cert; reason: sha1-cert; keyring refresh: still-fails |
| virt-v2v | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| virt-what | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| voikko-fi | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| volk | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: no-update |
| wayland | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| webkitgtk | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (remove); reason: expired; keyring refresh: proposed |
| weechat | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| weldr-client | `tested` | 1→1 | rawhide: both-pass |  |
| wget2 | `tested` | 1→1 | rawhide: both-pass |  |
| wl-mirror | `tested` | 1→1 | rawhide: both-pass |  |
| wlr-randr | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| wlroots | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| wlroots0.18 | `tested` | 1→1 | rawhide: both-pass |  |
| wlroots0.19 | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| wob | `tested` | 1→1 | rawhide: both-pass |  |
| xalan-c | `tested` | 1→1 | rawhide: both-pass |  |
| xcb-imdkit | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| xcb-util-errors | `regression` | 1→1 | rawhide: regression | reason: binding-after-signature; keyring refresh: still-fails |
| xclipboard | `tested` | 1→1 | rawhide: both-pass |  |
| xdg-desktop-portal-wlr | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| xdriinfo | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| xerces-c | `tested` | 1→1 | rawhide: both-pass |  |
| xev | `tested` | 1→1 | rawhide: both-pass |  |
| xforms | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| xfsdump | `tested` | 1→1 | rawhide: both-pass |  |
| xfsprogs | `tested` | 1→1 | rawhide: both-pass |  |
| xgamma | `tested` | 1→1 | rawhide: both-pass |  |
| xkeyboard-config | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| xkill | `tested` | 1→1 | rawhide: both-pass |  |
| xload | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| xlogo | `regression` | 1→1 | rawhide: regression | reason: weak-key |
| xlsclients | `tested` | 1→1 | rawhide: both-pass |  |
| xmag | `regression` | 1→1 | rawhide: regression | reason: weak-key |
| xmodmap | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| xorg-x11-drv-amdgpu | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: no-update |
| xpdf | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| xstdcmap | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| xterm | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| xvinfo | `tested` | 1→1 | rawhide: both-pass |  |
| xwd | `tested` | 1→1 | rawhide: both-pass |  |
| xwininfo | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| xwud | `tested` | 1→1 | rawhide: both-pass |  |
| xz | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| yambar | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| yascreen | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| yubico-piv-tool | `superseded` | -→- |  |  |
| yubihsm-connector | `superseded` | -→- |  |  |
| yubihsm-shell | `superseded` | -→- |  |  |
| yubikey-manager-qt | `superseded` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| zix | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| znc | `regression` | 2→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| zsh | `superseded` | -→- |  |  |
