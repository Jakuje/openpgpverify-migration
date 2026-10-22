# Phase 1 results

Generated 2026-10-22T11:12Z from `data/state/packages.jsonl`: 178 of 595 packages tested.

| Status | Packages |
|---|---|
| `tested` | 75 |
| `regression` | 74 |
| `manual` | 15 |
| `skipped` | 12 |
| `guard-failed` | 1 |
| `not-buildable` | 1 |

| Regression reason | Calls |
|---|---|
| `sha1-cert` | 43 |
| `sha1-sig` | 19 |
| `expired` | 14 |
| `unparseable-cert` | 6 |
| `weak-key` | 2 |
| `keybox` | 1 |
| `v3-sig` | 1 |
| `binding-after-signature` | 1 |

| Package | Status | Calls old→new | Chroots | Notes |
|---|---|---|---|---|
| SDL3 | `tested` | 1→1 | rawhide: both-pass, eln: both-pass |  |
| Xaw3d | `regression` | 1→1 | rawhide: regression | reason: weak-key |
| acl | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| aide | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| apache-commons-net | `regression` | 1→1 | rawhide: regression | reason: unparseable-cert |
| attr | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| autoconf-archive | `tested` | 1→1 | rawhide: both-pass |  |
| babeltrace2 | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| bash | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-sig |
| bc | `tested` | 1→1 | rawhide: both-pass |  |
| bind | `guard-failed` | 0→0 | rawhide: guard-failed, eln: not-verified | old spec executed no gpgverify call (prep rc 0); the unchanged spec does not verify sources in this chroot; B… |
| bison | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-sig |
| blktrace | `tested` | 1→1 | rawhide: both-pass |  |
| bzip2 | `inventory` | -→- |  |  |
| cairomm1.16 | `skipped` | -→- |  |  |
| checkpolicy | `skipped` | -→- |  |  |
| chrony | `tested` | 1→1 | rawhide: both-pass, eln: both-pass | BR gnupg2 kept (review) |
| cmocka | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| conntrack-tools | `tested` | 1→1 | rawhide: both-pass |  |
| coreutils | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| cpio | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-sig |
| crun | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| curl | `not-buildable` | 0→0 | rawhide: not-buildable, eln: not-buildable | unchanged spec: installdeps failed; unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| cyrus-imapd | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| dbus | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| debugedit | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: keybox |
| dhcpcd | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; rhel conditional: gpgverify kept for EPEL branches; BR gnupg2 kept (revie… |
| dialog | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| dnf | `tested` | 1→1 | rawhide: both-pass, eln: both-pass | BR gnupg2 kept (review) |
| dns-root-data | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| dos2unix | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| dotnet10.0 | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| e2fsprogs | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: unparseable-cert; reason: unparseable-cert |
| ed | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: sha1-sig; reason: sha1-sig |
| emacs | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| ethtool | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| expat | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| fapolicyd | `skipped` | 2→2 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; replaced conditional BR in place: BuildRequires: gpgverify; rhel conditio… |
| file | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: sha1-sig; reason: sha1-sig |
| findutils | `regression` | 1→1 | rawhide: regression | reason: unparseable-cert |
| fio | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed |
| fips-provider | `tested` | 1→1 | rawhide: both-pass, eln: both-pass | BR gnupg2 kept (review) |
| git | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; rhel conditional: gpgverify kept for EPEL branches; BR gnupg2 kept (revie… |
| git-lfs | `skipped` | -→- |  |  |
| gnulib-l10n | `tested` | 1→1 | rawhide: both-pass |  |
| gnupg2 | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| gnutls | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| gpgme | `manual` | 2→0 | rawhide: manual | raw verification baseline passes |
| grep | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| guestfs-tools | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| hivex | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: sha1-cert; reason: sha1-cert; keyring refresh: still-fails |
| httpd | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: unparseable-cert; reason: unparseable-cert |
| ibus-chewing | `tested` | 1→1 | rawhide: both-pass |  |
| iotop-c | `tested` | 1→1 | rawhide: both-pass |  |
| ipcalc | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| iptables | `tested` | 1→1 | rawhide: both-pass, eln: both-pass |  |
| irssi | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; reason: sha1-sig |
| kea | `skipped` | -→- |  |  |
| ldns | `tested` | 1→1 | rawhide: both-pass |  |
| libXpm | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-sig |
| libburn | `regression` | 1→1 | rawhide: regression, eln: regression | reason: sha1-sig; reason: sha1-sig |
| libcap | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| libchewing | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libdisplay-info | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| libdnf | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| libdvdnav | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| libdvdread | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| libgpg-error | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libguestfs | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| libidn2 | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| libisoburn | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: sha1-sig; reason: sha1-sig |
| libisofs | `regression` | 1→1 | rawhide: regression, eln: regression | reason: sha1-sig; reason: sha1-sig |
| libksba | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libmnl | `tested` | 1→1 | rawhide: both-pass |  |
| libmodulemd | `tested` | 1→1 | rawhide: both-pass, eln: both-pass | BR gnupg2 kept (review) |
| libmpc | `regression` | 1→1 | rawhide: regression | reason: weak-key |
| libnbd | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| libnetfilter_conntrack | `tested` | 1→1 | rawhide: both-pass |  |
| libnftnl | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libreswan | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| librhsm | `tested` | 1→1 | rawhide: both-pass |  |
| libselinux | `skipped` | -→- |  |  |
| libsemanage | `skipped` | -→- |  |  |
| libsepol | `skipped` | -→- |  |  |
| libssh | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libssh2 | `tested` | 1→1 | rawhide: both-pass, eln: both-pass | BR gnupg2 kept (review) |
| libtalloc | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| libtasn1 | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| libtdb | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| libtevent | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| libtpms | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| libusb1 | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libuv | `manual` | 1→0 | rawhide: manual, eln: manual | raw verification baseline passes; raw verification baseline passes |
| libvoikko | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| libxcrypt | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| llvm | `tested` | 2→2 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| llvm22 | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review) |
| log4cplus | `tested` | 1→1 | rawhide: both-pass |  |
| logrotate | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| lttng-ust | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| lynx | `tested` | 1→1 | rawhide: both-pass, eln: both-pass |  |
| man-db | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| mcstrans | `skipped` | -→- |  |  |
| mdadm | `tested` | 1→1 | rawhide: both-pass |  |
| mkfontscale | `inventory` | -→- |  |  |
| munge | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| nano | `tested` | 1→1 | rawhide: both-pass |  |
| nbdkit | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| ncurses | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; reason: expired; keyring refresh: proposed |
| nettle | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: still-fails |
| nftables | `tested` | 1→1 | rawhide: both-pass |  |
| nghttp2 | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: no-update |
| nginx | `skipped` | -→- |  |  |
| nmap | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| nmstate | `manual` | 2→0 | rawhide: manual, eln: manual | raw verification baseline passes; raw verification: no gpg call executed in baseline |
| npth | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| nss_wrapper | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| ocaml-augeas | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| openssh | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| p11-kit | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| pam_wrapper | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| parted | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| pcre2 | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| pcsc-lite | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: proposed |
| pcsc-lite-ccid | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| pdfio | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| php | `tested` | 1→1 | rawhide: both-pass, eln: both-pass | BR gnupg2 kept (review) |
| pinentry | `tested` | 1→1 | rawhide: both-pass, eln: both-pass |  |
| pkcs11-provider | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| policycoreutils | `skipped` | -→- |  |  |
| poppler | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: expired; reason: expired; keyring refresh: proposed |
| priv_wrapper | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| pyparted | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| pyxattr | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| radvd | `skipped` | -→- |  |  |
| resolv_wrapper | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| rust | `regression` | 1→1 | rawhide: regression, eln: regression | replaced conditional BR in place: BuildRequires:  gpgverify; rhel conditional: gpgverify kept for EPEL branch… |
| s-nail | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| samba | `manual` | 2→0 | rawhide: manual, eln: manual | raw verification baseline passes; raw verification: no gpg call executed in baseline |
| socket_wrapper | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| squid | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| sssd | `inventory` | -→- |  |  |
| stunnel | `regression` | 1→1 | rawhide: regression, eln: regression | BR gnupg2 kept (review); reason: sha1-cert; reason: sha1-cert; keyring refresh: still-fails |
| supermin | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| teckit | `skipped` | 0→0 | rawhide: guard-failed | old spec executed no gpgverify call (prep rc 0) |
| tftp | `skipped` | -→- |  |  |
| time | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: binding-after-signature; keyring refresh: proposed |
| tomcat | `tested` | 1→1 | rawhide: both-pass |  |
| tpm2-openssl | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| uid_wrapper | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: proposed |
| unbound | `tested` | 1→1 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; rhel conditional: gpgverify kept for EPEL branches; BR gnupg2 kept (revie… |
| usbredir | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| virt-p2v | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| virt-top | `regression` | 1→1 | rawhide: regression, eln: regression | reason: sha1-cert; reason: sha1-cert; keyring refresh: still-fails |
| virt-v2v | `regression` | 1→1 | rawhide: regression, eln: not-buildable | unchanged spec: installdeps failed; BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| virt-what | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: still-fails |
| voikko-fi | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: still-fails |
| wayland | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| xfsdump | `tested` | 1→1 | rawhide: both-pass |  |
| xfsprogs | `tested` | 1→1 | rawhide: both-pass |  |
| xkeyboard-config | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| xterm | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| xz | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: expired; keyring refresh: proposed |
| zsh | `skipped` | -→- |  |  |
