# Phase 1 results

Generated 2026-10-23T08:21Z from `data/state/packages.jsonl`: 328 of 595 packages tested.

| Status | Packages |
|---|---|
| `tested` | 166 |
| `regression` | 131 |
| `manual` | 16 |
| `skipped` | 12 |
| `guard-failed` | 2 |
| `not-buildable` | 1 |

| Regression reason | Calls |
|---|---|
| `sha1-cert` | 67 |
| `expired` | 35 |
| `sha1-sig` | 21 |
| `weak-key` | 9 |
| `unparseable-cert` | 7 |
| `v3-sig` | 4 |
| `binding-after-signature` | 2 |
| `keybox` | 1 |

| Package | Status | Calls old→new | Chroots | Notes |
|---|---|---|---|---|
| SDL3 | `tested` | 1→1 | rawhide: both-pass, eln: both-pass |  |
| Xaw3d | `regression` | 1→1 | rawhide: regression | reason: weak-key |
| abcde | `tested` | 1→1 | rawhide: both-pass |  |
| acl | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| aesfix | `regression` | 1→1 | rawhide: regression | reason: v3-sig |
| aeskeyfind | `regression` | 1→1 | rawhide: regression | reason: v3-sig |
| aide | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| anet | `tested` | 1→1 | rawhide: both-pass |  |
| ant-antunit | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: unparseable-cert |
| apache-commons-net | `regression` | 1→1 | rawhide: regression | reason: unparseable-cert |
| apachetop | `tested` | 1→1 | rawhide: both-pass |  |
| attr | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| autoconf-archive | `tested` | 1→1 | rawhide: both-pass |  |
| b43-fwcutter | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| babeltrace2 | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| basez | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| bash | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-sig |
| batctl | `tested` | 1→1 | rawhide: both-pass |  |
| bc | `tested` | 1→1 | rawhide: both-pass |  |
| bemenu | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| bind | `guard-failed` | 0→0 | rawhide: guard-failed, eln: not-verified | old spec executed no gpgverify call (prep rc 0); the unchanged spec does not verify sources in this chroot; B… |
| bison | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-sig |
| blktrace | `tested` | 1→1 | rawhide: both-pass |  |
| bpfmon | `tested` | 1→1 | rawhide: both-pass |  |
| budgie-desktop-defaults | `tested` | 1→1 | rawhide: both-pass |  |
| cage | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| cairomm1.16 | `skipped` | -→- |  |  |
| checkpolicy | `skipped` | -→- |  |  |
| chewing-editor | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| chrony | `tested` | 1→1 | rawhide: both-pass, eln: both-pass | BR gnupg2 kept (review) |
| cksfv | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| cmocka | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| conflict | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| conntrack-tools | `tested` | 1→1 | rawhide: both-pass |  |
| coreutils | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| cpio | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-sig |
| cproto | `tested` | 1→1 | rawhide: both-pass |  |
| crun | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| cscppc | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| csmock | `tested` | 1→1 | rawhide: both-pass |  |
| cswrap | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| ctstream | `tested` | 1→1 | rawhide: both-pass |  |
| curl | `not-buildable` | 0→0 | rawhide: not-buildable, eln: not-buildable | unchanged spec: installdeps failed; unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| cyrus-imapd | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| dbus | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| dbus-glib | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| dbus-python | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| debugedit | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: keybox |
| dehydrated | `tested` | 1→1 | rawhide: both-pass |  |
| dhcpcd | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: sha1-cert; reason: sha1-cert; keyring refresh: proposed |
| dhcpdump | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| dialog | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| dnf | `tested` | 1→1 | rawhide: both-pass, eln: both-pass | BR gnupg2 kept (review) |
| dns-root-data | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| dos2unix | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| dotnet10.0 | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| drm_info | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| e2fsprogs | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: unparseable-cert; reason: unparseable-cert |
| ed | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: sha1-sig; reason: sha1-sig |
| emacs | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| ethtool | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| expat | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| facter | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| fapolicyd | `skipped` | 2→2 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; replaced conditional BR in place: BuildRequires: gpgverify; rhel conditio… |
| fcitx5-anthy | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| fcitx5-chewing | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
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
| fcitx5-unikey | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| file | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: sha1-sig; reason: sha1-sig |
| findutils | `regression` | 1→1 | rawhide: regression | reason: unparseable-cert |
| fio | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed |
| fips-provider | `tested` | 1→1 | rawhide: both-pass, eln: both-pass | BR gnupg2 kept (review) |
| fuse-sshfs | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| gencolormap | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| getdns | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| git | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: sha1-cert; reason: sha1-cert; keyring refresh: proposed |
| glinf | `regression` | 1→1 | rawhide: regression | reason: binding-after-signature; keyring refresh: still-fails |
| gnulib-l10n | `tested` | 1→1 | rawhide: both-pass |  |
| gnupg2 | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| gnutls | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| gpgme | `manual` | 2→0 | rawhide: manual | raw verification baseline passes |
| gpgmepp | `tested` | 1→1 | rawhide: both-pass |  |
| gplugin | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| grep | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| grim | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| guestfs-tools | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| hcxtools | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| hiera | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| hivex | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: sha1-cert; reason: sha1-cert; keyring refresh: still-fails |
| httpd | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: unparseable-cert; reason: unparseable-cert |
| i3lock | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| i3status | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| ibus-chewing | `tested` | 1→1 | rawhide: both-pass |  |
| iotop-c | `tested` | 1→1 | rawhide: both-pass |  |
| ipcalc | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| iptables | `tested` | 1→1 | rawhide: both-pass, eln: both-pass |  |
| irssi | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; reason: sha1-sig |
| jalv | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| kanshi | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| kea | `skipped` | -→- |  |  |
| kio-fuse | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| kronometer | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| ldns | `tested` | 1→1 | rawhide: both-pass |  |
| libXpm | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-sig |
| libburn | `regression` | 1→1 | rawhide: regression, eln: regression | reason: sha1-sig; reason: sha1-sig |
| libcap | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| libchewing | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libdisplay-info | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| libdnf | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| libdvdnav | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| libdvdread | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| libgnt | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libgpg-error | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libguestfs | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| libidn2 | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| libisoburn | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: sha1-sig; reason: sha1-sig |
| libisofs | `regression` | 1→1 | rawhide: regression, eln: regression | reason: sha1-sig; reason: sha1-sig |
| libksba | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| liblxi | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| libmnl | `tested` | 1→1 | rawhide: both-pass |  |
| libmodulemd | `tested` | 1→1 | rawhide: both-pass, eln: both-pass | BR gnupg2 kept (review) |
| libmpc | `regression` | 1→1 | rawhide: regression | reason: weak-key |
| libnbd | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| libnetfilter_conntrack | `tested` | 1→1 | rawhide: both-pass |  |
| libnftnl | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libnids | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| libptytty | `tested` | 1→1 | rawhide: both-pass |  |
| libredwg | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| libreswan | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| librhsm | `tested` | 1→1 | rawhide: both-pass |  |
| libselinux | `skipped` | -→- |  |  |
| libsemanage | `skipped` | -→- |  |  |
| libssh | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libssh2 | `tested` | 1→1 | rawhide: both-pass, eln: both-pass | BR gnupg2 kept (review) |
| libstrophe | `tested` | 1→1 | rawhide: both-pass |  |
| libtalloc | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| libtasn1 | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| libtdb | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| libtevent | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| libtpms | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| libusb1 | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libuv | `manual` | 1→0 | rawhide: manual, eln: manual | raw verification baseline passes; raw verification baseline passes |
| libvoikko | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| libxcrypt | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| lilv | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| llvm | `tested` | 2→2 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| llvm22 | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| log4cplus | `tested` | 1→1 | rawhide: both-pass |  |
| logrotate | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| lttng-ust | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| lua-unbound | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| lynx | `tested` | 1→1 | rawhide: both-pass, eln: both-pass |  |
| mako | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| man-db | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| maven-reporting-api | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| mcstrans | `skipped` | -→- |  |  |
| mdadm | `tested` | 1→1 | rawhide: both-pass |  |
| mingw-cmocka | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| mingw-usbredir | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| mooltipass-udev | `tested` | 1→1 | rawhide: both-pass |  |
| mpdscribble | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| mucalc | `tested` | 1→1 | rawhide: both-pass |  |
| munge | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| nano | `tested` | 1→1 | rawhide: both-pass |  |
| nbdkit | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| ncurses | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; reason: expired; keyring refresh: proposed |
| nettle | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: still-fails |
| nftables | `tested` | 1→1 | rawhide: both-pass |  |
| nghttp2 | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: no-update |
| nginx-mod-fancyindex | `regression` | 1→1 | rawhide: regression | reason: weak-key |
| nmap | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| nmstate | `manual` | 2→0 | rawhide: manual, eln: manual | raw verification baseline passes; raw verification: no gpg call executed in baseline |
| npth | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| nss-pem | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| nss_wrapper | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| ocaml-augeas | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| ocaml-mysql | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| oclock | `regression` | 1→1 | rawhide: regression | reason: weak-key |
| oidentd | `tested` | 1→1 | rawhide: both-pass |  |
| opendoas | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: still-fails |
| openresolv | `regression` | 1→1 | rawhide: regression, eln: regression | reason: sha1-cert; reason: sha1-cert; keyring refresh: proposed |
| openssh | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| openssl-pkcs11 | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| p11-kit | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| pam_wrapper | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| pari-galdata | `regression` | 1→1 | rawhide: regression | reason: v3-sig |
| parted | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| pass-audit | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| pcre2 | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| pcsc-lite | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| pcsc-lite-ccid | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| pdfgrep | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: weak-key |
| pdfio | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| perl-WWW-OrangeHRM-Client | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: weak-key |
| php | `tested` | 1→1 | rawhide: both-pass, eln: both-pass | BR gnupg2 kept (review) |
| pianobar | `tested` | 1→1 | rawhide: both-pass |  |
| pinentry | `tested` | 1→1 | rawhide: both-pass, eln: both-pass |  |
| pkcs11-provider | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| policycoreutils | `skipped` | -→- |  |  |
| poppler | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: expired; reason: expired; keyring refresh: proposed |
| postfix-mta-sts-resolver | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| priv_wrapper | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| pylibacl | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| pyparted | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| python-aodhclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-authres | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| python-automaton | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-barbicanclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:    gpgverify |
| python-debtcollector | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-dijitso | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: no-update |
| python-ezgb | `tested` | 1→1 | rawhide: both-pass |  |
| python-futurist | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  gpgverify |
| python-gnocchiclient | `guard-failed` | 0→0 | rawhide: guard-failed | old spec executed no gpgverify call (prep rc 0); dropped conditional BR: BuildRequires:  /usr/bin/gpgv2; no u… |
| python-gnupg | `tested` | 1→1 | rawhide: both-pass | no unconditional BuildRequires; BR added before first section; BR gnupg2 kept (review) |
| python-hacking | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2; no unconditional BuildRequires; BR added before first… |
| python-heatclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-liblore | `tested` | 1→1 | rawhide: both-pass |  |
| python-libusb1 | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| python-magnumclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:    /usr/bin/gpgv2 |
| python-mistralclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-neutronclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-octaviaclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
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
| python-patatt | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| python-pskc | `tested` | 1→1 | rawhide: both-pass |  |
| python-reno | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-swiftclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-tackerclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-troveclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-zaqarclient | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| python-zstarfile | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| pyxattr | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| qemu-sanity-check | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| qgpgme | `tested` | 1→1 | rawhide: both-pass |  |
| radvd | `skipped` | -→- |  |  |
| resolv_wrapper | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| rhythmbox-alternative-toolbar | `tested` | 1→1 | rawhide: both-pass |  |
| rpminspect-data-centos | `tested` | 1→1 | rawhide: both-pass |  |
| rsakeyfind | `regression` | 1→1 | rawhide: regression | reason: v3-sig |
| rust | `regression` | 1→1 | rawhide: regression, eln: regression | dropped conditional BR: BuildRequires:  gpgverify; BR gnupg2 kept (review); reason: sha1-cert; reason: sha1-c… |
| s-nail | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| samba | `manual` | 2→0 | rawhide: manual, eln: manual | raw verification baseline passes; raw verification: no gpg call executed in baseline |
| screenkey | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| secilc | `tested` | 1→1 | rawhide: both-pass |  |
| serd | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| setxkbmap | `tested` | 1→1 | rawhide: both-pass |  |
| signify | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: weak-key |
| slurp | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| socket_wrapper | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| sord | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| squid | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| sratom | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| ssh-audit | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| stunnel | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: sha1-cert; reason: sha1-cert; keyring refresh: still-fails |
| suil | `tested` | 1→1 | rawhide: both-pass |  |
| supermin | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| swaybg | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| swayidle | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| swaylock | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| sysconftool | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| teckit | `skipped` | 0→0 | rawhide: guard-failed | old spec executed no gpgverify call (prep rc 0) |
| tftp | `skipped` | -→- |  |  |
| time | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: binding-after-signature; keyring refresh: proposed |
| tomcat | `tested` | 1→1 | rawhide: both-pass |  |
| tomcli | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| tpm2-openssl | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| trojan | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| uid_wrapper | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| unbound | `tested` | 1→1 | rawhide: both-pass, eln: both-pass | BR gnupg2 kept (review) |
| usbredir | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| vali | `tested` | 1→1 | rawhide: both-pass |  |
| vim-latex | `tested` | 1→1 | rawhide: both-pass |  |
| virt-p2v | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| virt-top | `regression` | 1→1 | rawhide: regression, eln: regression | reason: sha1-cert; reason: sha1-cert; keyring refresh: still-fails |
| virt-v2v | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| virt-what | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| voikko-fi | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| wayland | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| wlr-randr | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| wob | `tested` | 1→1 | rawhide: both-pass |  |
| xclipboard | `tested` | 1→1 | rawhide: both-pass |  |
| xdg-desktop-portal-wlr | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| xdriinfo | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| xev | `tested` | 1→1 | rawhide: both-pass |  |
| xfsdump | `tested` | 1→1 | rawhide: both-pass |  |
| xfsprogs | `tested` | 1→1 | rawhide: both-pass |  |
| xgamma | `tested` | 1→1 | rawhide: both-pass |  |
| xkeyboard-config | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| xkill | `tested` | 1→1 | rawhide: both-pass |  |
| xload | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| xlogo | `regression` | 1→1 | rawhide: regression | reason: weak-key |
| xlsclients | `tested` | 1→1 | rawhide: both-pass |  |
| xmag | `regression` | 1→1 | rawhide: regression | reason: weak-key |
| xmodmap | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| xorg-x11-drv-amdgpu | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: no-update |
| xstdcmap | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| xterm | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| xvinfo | `tested` | 1→1 | rawhide: both-pass |  |
| xwd | `tested` | 1→1 | rawhide: both-pass |  |
| xwininfo | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| xwud | `tested` | 1→1 | rawhide: both-pass |  |
| xz | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| yambar | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| yascreen | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| yubikey-manager-qt | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| zix | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| zsh | `skipped` | -→- |  |  |
