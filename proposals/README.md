# Proposals

Generated 2026-10-26T07:28Z by `scripts/render_proposals.py` from the Phase 1 state. Nothing here has been opened or filed.

- **PR**: `0001-*.patch` is the commit a PR would carry (`git am` applies it to dist-git at the tested commit); `PR.md` is the PR title and description.
- **draft PR**: the same, but it includes a keyring refresh that hasn't been reviewed yet.
- **bug**: `BUG.md`, the Bugzilla fields and description for packages that need upstream or maintainer action first.

| Package | Proposal | Notes |
|---|---|---|
| gnupg2 | skipped | superseded: converted in dist-git (snapshot 2026-10-26) |
| libgpg-error | skipped | superseded: converted in dist-git (snapshot 2026-10-26) |
| libksba | skipped | superseded: converted in dist-git (snapshot 2026-10-26) |
| libssh | skipped | superseded: converted in dist-git (snapshot 2026-10-26) |
| [openssl-pkcs11](openssl-pkcs11/) | bug | sha1-cert |
| pinentry | skipped | superseded: converted in dist-git (snapshot 2026-10-26) |
| yubikey-manager-qt | skipped | superseded: converted in dist-git (snapshot 2026-10-26) |
| openssh | skipped | superseded: converted in dist-git (snapshot 2026-10-26) |
| pcsc-lite-ccid | skipped | manual: fedora-rawhide-x86_64: manual (raw verification baseline passes) |
| [wob](wob/) | PR |  |
| [getdns](getdns/) | bug | sha1-cert |
| [python-ezgb](python-ezgb/) | PR |  |
| [dns-root-data](dns-root-data/) | bug | sha1-sig |
| [libstrophe](libstrophe/) | PR |  |
| [openresolv](openresolv/) | draft PR | keyring refresh proposed |
| fapolicyd | skipped | superseded: converted in dist-git (snapshot 2026-10-26) |
| [python-oslo-metrics](python-oslo-metrics/) | PR |  |
| [mpdscribble](mpdscribble/) | bug | sha1-cert |
| [rsakeyfind](rsakeyfind/) | bug | v3-sig |
| [vali](vali/) | PR |  |
| [mooltipass-udev](mooltipass-udev/) | PR |  |
| [basez](basez/) | PR |  |
| [hiera](hiera/) | PR |  |
| [kio-fuse](kio-fuse/) | PR |  |
| [i3status](i3status/) | PR |  |
| [conflict](conflict/) | PR |  |
| [ssh-audit](ssh-audit/) | PR |  |
| logrotate | skipped | open PR exists: https://src.fedoraproject.org/rpms/logrotate/pull-request/4 |
| [vim-latex](vim-latex/) | PR |  |
| libmnl | skipped | open PR exists: https://src.fedoraproject.org/rpms/libmnl/pull-request/4 |
| [time](time/) | draft PR | keyring refresh proposed |
| [dbus-glib](dbus-glib/) | PR |  |
| gnulib-l10n | skipped | open PR exists: https://src.fedoraproject.org/rpms/gnulib-l10n/pull-request/1 |
| radvd | skipped | open PR exists: https://src.fedoraproject.org/rpms/radvd/pull-request/17 |
| dbus | skipped | open PR exists: https://src.fedoraproject.org/rpms/dbus/pull-request/21 |
| SDL3 | skipped | open PR exists: https://src.fedoraproject.org/rpms/SDL3/pull-request/4 |
| [Xaw3d](Xaw3d/) | bug | weak-key |
| acl | skipped | open PR exists: https://src.fedoraproject.org/rpms/acl/pull-request/10 |
| [aide](aide/) | draft PR | keyring refresh proposed |
| [apache-commons-net](apache-commons-net/) | bug | unparseable-cert |
| attr | skipped | open PR exists: https://src.fedoraproject.org/rpms/attr/pull-request/7 |
| autoconf-archive | skipped | open PR exists: https://src.fedoraproject.org/rpms/autoconf-archive/pull-request/8 |
| [babeltrace2](babeltrace2/) | draft PR | keyring refresh proposed |
| [bash](bash/) | bug | sha1-sig |
| bc | skipped | open PR exists: https://src.fedoraproject.org/rpms/bc/pull-request/9 |
| bind | skipped | guard-failed: fedora-rawhide-x86_64: guard-failed (old spec executed no gpgverify call (prep rc 0)); fedora-eln-x86_64: not-verified (the unchanged spec does not verify sources in this chroot) |
| [bison](bison/) | bug | sha1-sig |
| blktrace | skipped | open PR exists: https://src.fedoraproject.org/rpms/blktrace/pull-request/8 |
| bzip2 | skipped | open PR exists: https://src.fedoraproject.org/rpms/bzip2/pull-request/4 |
| cairomm1.16 | skipped | superseded: converted in dist-git (snapshot 2026-10-26) |
| checkpolicy | skipped | open PR exists: https://src.fedoraproject.org/rpms/checkpolicy/pull-request/12 |
| chrony | skipped | open PR exists: https://src.fedoraproject.org/rpms/chrony/pull-request/15 |
| [cmocka](cmocka/) | draft PR | keyring refresh proposed |
| conntrack-tools | skipped | open PR exists: https://src.fedoraproject.org/rpms/conntrack-tools/pull-request/5 |
| [coreutils](coreutils/) | bug | sha1-cert |
| [cpio](cpio/) | bug | sha1-sig |
| crun | skipped | open PR exists: https://src.fedoraproject.org/rpms/crun/pull-request/159 |
| curl | skipped | not-buildable: fedora-rawhide-x86_64: not-buildable (unchanged spec: installdeps failed); fedora-eln-x86_64: not-buildable (unchanged spec: installdeps failed) |
| [cyrus-imapd](cyrus-imapd/) | bug | sha1-cert |
| [debugedit](debugedit/) | bug | keybox |
| [dhcpcd](dhcpcd/) | draft PR | keyring refresh proposed |
| [dialog](dialog/) | draft PR | keyring refresh proposed |
| dnf | skipped | open PR exists: https://src.fedoraproject.org/rpms/dnf/pull-request/28 |
| [dos2unix](dos2unix/) | bug | sha1-cert |
| dotnet10.0 | skipped | dist-git changed since Phase 1; re-run it |
| [e2fsprogs](e2fsprogs/) | bug | unparseable-cert |
| [ed](ed/) | bug | sha1-sig |
| emacs | skipped | open PR exists: https://src.fedoraproject.org/rpms/emacs/pull-request/51 |
| ethtool | skipped | open PR exists: https://src.fedoraproject.org/rpms/ethtool/pull-request/9 |
| [expat](expat/) | draft PR | keyring refresh proposed |
| [file](file/) | bug | sha1-sig |
| [findutils](findutils/) | bug | unparseable-cert |
| fio | skipped | open PR exists: https://src.fedoraproject.org/rpms/fio/pull-request/20 |
| fips-provider | skipped | open PR exists: https://src.fedoraproject.org/rpms/fips-provider/pull-request/3 |
| [git](git/) | draft PR | keyring refresh proposed |
| git-lfs | skipped | open PR exists: https://src.fedoraproject.org/rpms/git-lfs/pull-request/9 |
| gnutls | skipped | open PR exists: https://src.fedoraproject.org/rpms/gnutls/pull-request/188 |
| gpgme | skipped | manual: fedora-rawhide-x86_64: manual (raw verification baseline passes) |
| grep | skipped | open PR exists: https://src.fedoraproject.org/rpms/grep/pull-request/6 |
| [guestfs-tools](guestfs-tools/) | bug | sha1-cert |
| [hivex](hivex/) | bug | sha1-cert |
| [httpd](httpd/) | bug | unparseable-cert |
| ibus-chewing | skipped | open PR exists: https://src.fedoraproject.org/rpms/ibus-chewing/pull-request/4 |
| iotop-c | skipped | open PR exists: https://src.fedoraproject.org/rpms/iotop-c/pull-request/2 |
| [ipcalc](ipcalc/) | draft PR | keyring refresh proposed |
| iptables | skipped | open PR exists: https://src.fedoraproject.org/rpms/iptables/pull-request/18 |
| [irssi](irssi/) | bug | sha1-sig |
| kea | skipped | open PR exists: https://src.fedoraproject.org/rpms/kea/pull-request/72 |
| ldns | skipped | open PR exists: https://src.fedoraproject.org/rpms/ldns/pull-request/10 |
| [libXpm](libXpm/) | bug | sha1-sig |
| [libburn](libburn/) | bug | sha1-sig |
| [libcap](libcap/) | draft PR | keyring refresh proposed |
| libchewing | skipped | open PR exists: https://src.fedoraproject.org/rpms/libchewing/pull-request/9 |
| [libdisplay-info](libdisplay-info/) | draft PR | keyring refresh proposed |
| libdnf | skipped | open PR exists: https://src.fedoraproject.org/rpms/libdnf/pull-request/14 |
| [libdvdnav](libdvdnav/) | bug | sha1-sig |
| [libdvdread](libdvdread/) | bug | sha1-sig |
| [libguestfs](libguestfs/) | bug | sha1-cert |
| [libidn2](libidn2/) | draft PR | keyring refresh proposed |
| [libisoburn](libisoburn/) | bug | sha1-sig |
| [libisofs](libisofs/) | bug | sha1-sig |
| libmodulemd | skipped | superseded: converted in dist-git (snapshot 2026-10-26) |
| [libmpc](libmpc/) | bug | weak-key |
| [libnbd](libnbd/) | bug | sha1-cert |
| libnetfilter_conntrack | skipped | open PR exists: https://src.fedoraproject.org/rpms/libnetfilter_conntrack/pull-request/4 |
| libnftnl | skipped | open PR exists: https://src.fedoraproject.org/rpms/libnftnl/pull-request/3 |
| libreswan | skipped | open PR exists: https://src.fedoraproject.org/rpms/libreswan/pull-request/14 |
| librhsm | skipped | open PR exists: https://src.fedoraproject.org/rpms/librhsm/pull-request/3 |
| libselinux | skipped | open PR exists: https://src.fedoraproject.org/rpms/libselinux/pull-request/45 |
| libsemanage | skipped | open PR exists: https://src.fedoraproject.org/rpms/libsemanage/pull-request/24 |
| libsepol | skipped | open PR exists: https://src.fedoraproject.org/rpms/libsepol/pull-request/30 |
| libssh2 | skipped | open PR exists: https://src.fedoraproject.org/rpms/libssh2/pull-request/4 |
| libtalloc | skipped | manual: fedora-rawhide-x86_64: manual (raw verification baseline passes) |
| libtasn1 | skipped | manual: fedora-rawhide-x86_64: manual (raw verification baseline passes) |
| libtdb | skipped | manual: fedora-rawhide-x86_64: manual (raw verification baseline passes) |
| libtevent | skipped | manual: fedora-rawhide-x86_64: manual (raw verification baseline passes) |
| [libtpms](libtpms/) | bug | sha1-cert |
| libusb1 | skipped | open PR exists: https://src.fedoraproject.org/rpms/libusb1/pull-request/11 |
| libuv | skipped | manual: fedora-rawhide-x86_64: manual (raw verification baseline passes); fedora-eln-x86_64: manual (raw verification baseline passes) |
| [libvoikko](libvoikko/) | bug | sha1-cert |
| libxcrypt | skipped | open PR exists: https://src.fedoraproject.org/rpms/libxcrypt/pull-request/23 |
| llvm | skipped | open PR exists: https://src.fedoraproject.org/rpms/llvm/pull-request/670 |
| llvm22 | skipped | open PR exists: https://src.fedoraproject.org/rpms/llvm22/pull-request/3 |
| log4cplus | skipped | open PR exists: https://src.fedoraproject.org/rpms/log4cplus/pull-request/13 |
| lttng-ust | skipped | open PR exists: https://src.fedoraproject.org/rpms/lttng-ust/pull-request/3 |
| lynx | skipped | open PR exists: https://src.fedoraproject.org/rpms/lynx/pull-request/8 |
| man-db | skipped | open PR exists: https://src.fedoraproject.org/rpms/man-db/pull-request/22 |
| mcstrans | skipped | open PR exists: https://src.fedoraproject.org/rpms/mcstrans/pull-request/6 |
| mdadm | skipped | open PR exists: https://src.fedoraproject.org/rpms/mdadm/pull-request/14 |
| mkfontscale | skipped | open PR exists: https://src.fedoraproject.org/rpms/mkfontscale/pull-request/2 |
| munge | skipped | open PR exists: https://src.fedoraproject.org/rpms/munge/pull-request/11 |
| nano | skipped | open PR exists: https://src.fedoraproject.org/rpms/nano/pull-request/9 |
| [nbdkit](nbdkit/) | bug | sha1-cert |
| [ncurses](ncurses/) | draft PR | keyring refresh proposed |
| [nettle](nettle/) | bug | expired |
| nftables | skipped | open PR exists: https://src.fedoraproject.org/rpms/nftables/pull-request/7 |
| [nghttp2](nghttp2/) | bug | sha1-cert |
| nginx | skipped | superseded: converted in dist-git (snapshot 2026-10-26) |
| [nmap](nmap/) | bug | sha1-sig |
| nmstate | skipped | manual: fedora-rawhide-x86_64: manual (raw verification baseline passes); fedora-eln-x86_64: manual (raw verification: no gpg call executed in baseline) |
| npth | skipped | superseded: converted in dist-git (snapshot 2026-10-26) |
| [nss_wrapper](nss_wrapper/) | draft PR | keyring refresh proposed |
| [ocaml-augeas](ocaml-augeas/) | bug | sha1-cert |
| p11-kit | skipped | manual: fedora-rawhide-x86_64: manual (raw verification baseline passes) |
| [pam_wrapper](pam_wrapper/) | draft PR | keyring refresh proposed |
| parted | skipped | open PR exists: https://src.fedoraproject.org/rpms/parted/pull-request/9 |
| pcre2 | skipped | open PR exists: https://src.fedoraproject.org/rpms/pcre2/pull-request/39 |
| [pcsc-lite](pcsc-lite/) | draft PR | keyring refresh proposed |
| [pdfio](pdfio/) | draft PR | keyring refresh proposed |
| php | skipped | open PR exists: https://src.fedoraproject.org/rpms/php/pull-request/9 |
| pkcs11-provider | skipped | superseded: converted in dist-git (snapshot 2026-10-26) |
| policycoreutils | skipped | open PR exists: https://src.fedoraproject.org/rpms/policycoreutils/pull-request/69 |
| [poppler](poppler/) | draft PR | keyring refresh proposed |
| [priv_wrapper](priv_wrapper/) | draft PR | keyring refresh proposed |
| pyparted | skipped | manual: fedora-rawhide-x86_64: manual (raw verification baseline passes) |
| pyxattr | skipped | open PR exists: https://src.fedoraproject.org/rpms/pyxattr/pull-request/8 |
| [resolv_wrapper](resolv_wrapper/) | draft PR | keyring refresh proposed |
| [rust](rust/) | bug | sha1-cert |
| [s-nail](s-nail/) | bug | sha1-cert |
| samba | skipped | manual: fedora-rawhide-x86_64: manual (raw verification baseline passes); fedora-eln-x86_64: manual (raw verification: no gpg call executed in baseline) |
| [socket_wrapper](socket_wrapper/) | draft PR | keyring refresh proposed |
| squid | skipped | open PR exists: https://src.fedoraproject.org/rpms/squid/pull-request/10 |
| sssd | skipped | open PR exists: https://src.fedoraproject.org/rpms/sssd/pull-request/94 |
| [stunnel](stunnel/) | bug | sha1-cert |
| [supermin](supermin/) | bug | sha1-cert |
| teckit | skipped | skipped: fedora-rawhide-x86_64: guard-failed (old spec executed no gpgverify call (prep rc 0)) |
| tftp | skipped | open PR exists: https://src.fedoraproject.org/rpms/tftp/pull-request/10 |
| tomcat | skipped | open PR exists: https://src.fedoraproject.org/rpms/tomcat/pull-request/104 |
| tpm2-openssl | skipped | manual: fedora-rawhide-x86_64: manual (raw verification baseline passes) |
| [uid_wrapper](uid_wrapper/) | draft PR | keyring refresh proposed |
| unbound | skipped | open PR exists: https://src.fedoraproject.org/rpms/unbound/pull-request/41 |
| usbredir | skipped | manual: fedora-rawhide-x86_64: manual (raw verification baseline passes) |
| [virt-p2v](virt-p2v/) | bug | sha1-cert |
| [virt-top](virt-top/) | bug | sha1-cert |
| [virt-v2v](virt-v2v/) | bug | sha1-cert |
| [virt-what](virt-what/) | bug | sha1-cert |
| [voikko-fi](voikko-fi/) | bug | sha1-cert |
| [wayland](wayland/) | draft PR | keyring refresh proposed |
| xfsdump | skipped | open PR exists: https://src.fedoraproject.org/rpms/xfsdump/pull-request/6 |
| xfsprogs | skipped | open PR exists: https://src.fedoraproject.org/rpms/xfsprogs/pull-request/30 |
| xkeyboard-config | skipped | manual: fedora-rawhide-x86_64: manual (raw verification baseline passes) |
| [xterm](xterm/) | draft PR | keyring refresh proposed |
| [xz](xz/) | draft PR | keyring refresh proposed |
| zsh | skipped | open PR exists: https://src.fedoraproject.org/rpms/zsh/pull-request/13 |
| [abcde](abcde/) | PR |  |
| [aesfix](aesfix/) | bug | v3-sig |
| [aeskeyfind](aeskeyfind/) | bug | v3-sig |
| [anet](anet/) | PR |  |
| [ant-antunit](ant-antunit/) | bug | unparseable-cert |
| [apachetop](apachetop/) | PR |  |
| [b43-fwcutter](b43-fwcutter/) | draft PR | keyring refresh proposed |
| [batctl](batctl/) | PR |  |
| [bemenu](bemenu/) | draft PR | keyring refresh proposed |
| [bpfmon](bpfmon/) | PR |  |
| [budgie-desktop-defaults](budgie-desktop-defaults/) | PR |  |
| [cage](cage/) | draft PR | keyring refresh proposed |
| [chewing-editor](chewing-editor/) | PR |  |
| [cksfv](cksfv/) | PR |  |
| [cproto](cproto/) | PR |  |
| [cscppc](cscppc/) | draft PR | keyring refresh proposed |
| [csmock](csmock/) | PR |  |
| [cswrap](cswrap/) | draft PR | keyring refresh proposed |
| ctstream | skipped | superseded: converted in dist-git (snapshot 2026-10-26) |
| [dbus-python](dbus-python/) | PR |  |
| [dehydrated](dehydrated/) | PR |  |
| [dhcpdump](dhcpdump/) | draft PR | keyring refresh proposed |
| [drm_info](drm_info/) | draft PR | keyring refresh proposed |
| [facter](facter/) | PR |  |
| [fcitx5-anthy](fcitx5-anthy/) | draft PR | keyring refresh proposed |
| [fcitx5-chewing](fcitx5-chewing/) | draft PR | keyring refresh proposed |
| [fcitx5-configtool](fcitx5-configtool/) | draft PR | keyring refresh proposed |
| [fcitx5-gtk](fcitx5-gtk/) | draft PR | keyring refresh proposed |
| [fcitx5-hangul](fcitx5-hangul/) | draft PR | keyring refresh proposed |
| [fcitx5-kkc](fcitx5-kkc/) | draft PR | keyring refresh proposed |
| [fcitx5-libthai](fcitx5-libthai/) | draft PR | keyring refresh proposed |
| [fcitx5-lua](fcitx5-lua/) | draft PR | keyring refresh proposed |
| [fcitx5-m17n](fcitx5-m17n/) | draft PR | keyring refresh proposed |
| [fcitx5-qt](fcitx5-qt/) | draft PR | keyring refresh proposed |
| [fcitx5-rime](fcitx5-rime/) | draft PR | keyring refresh proposed |
| [fcitx5-sayura](fcitx5-sayura/) | draft PR | keyring refresh proposed |
| [fcitx5-skk](fcitx5-skk/) | draft PR | keyring refresh proposed |
| [fcitx5-unikey](fcitx5-unikey/) | draft PR | keyring refresh proposed |
| [fuse-sshfs](fuse-sshfs/) | PR |  |
| [gencolormap](gencolormap/) | PR |  |
| [glinf](glinf/) | bug | binding-after-signature |
| [gpgmepp](gpgmepp/) | PR |  |
| [gplugin](gplugin/) | PR |  |
| grim | skipped | superseded: converted in dist-git (snapshot 2026-10-26) |
| [hcxtools](hcxtools/) | bug | sha1-cert |
| [i3lock](i3lock/) | draft PR | keyring refresh proposed |
| [jalv](jalv/) | PR |  |
| [kanshi](kanshi/) | draft PR | keyring refresh proposed |
| [kronometer](kronometer/) | PR |  |
| [libgnt](libgnt/) | PR |  |
| [liblxi](liblxi/) | bug | sha1-cert |
| [libnids](libnids/) | bug | sha1-sig |
| [libptytty](libptytty/) | PR |  |
| [libredwg](libredwg/) | draft PR | keyring refresh proposed |
| [lilv](lilv/) | PR |  |
| [lua-unbound](lua-unbound/) | PR |  |
| [mako](mako/) | draft PR | keyring refresh proposed |
| [maven-reporting-api](maven-reporting-api/) | draft PR | keyring refresh proposed |
| [mingw-cmocka](mingw-cmocka/) | draft PR | keyring refresh proposed |
| mingw-usbredir | skipped | manual: fedora-rawhide-x86_64: manual (raw verification baseline passes) |
| [mucalc](mucalc/) | PR |  |
| [nginx-mod-fancyindex](nginx-mod-fancyindex/) | bug | weak-key |
| [nss-pem](nss-pem/) | draft PR | keyring refresh proposed |
| [ocaml-mysql](ocaml-mysql/) | bug | sha1-sig |
| [oclock](oclock/) | bug | weak-key |
| [oidentd](oidentd/) | PR |  |
| [opendoas](opendoas/) | bug | expired |
| [pari-galdata](pari-galdata/) | bug | v3-sig |
| [pass-audit](pass-audit/) | PR |  |
| [pdfgrep](pdfgrep/) | bug | weak-key |
| [perl-WWW-OrangeHRM-Client](perl-WWW-OrangeHRM-Client/) | bug | weak-key |
| [pianobar](pianobar/) | PR |  |
| [postfix-mta-sts-resolver](postfix-mta-sts-resolver/) | PR |  |
| [pylibacl](pylibacl/) | PR |  |
| [python-aodhclient](python-aodhclient/) | PR |  |
| [python-authres](python-authres/) | PR |  |
| [python-automaton](python-automaton/) | PR |  |
| [python-barbicanclient](python-barbicanclient/) | PR |  |
| [python-debtcollector](python-debtcollector/) | PR |  |
| [python-dijitso](python-dijitso/) | bug | sha1-cert |
| [python-futurist](python-futurist/) | PR |  |
| python-gnocchiclient | skipped | guard-failed: fedora-rawhide-x86_64: guard-failed (old spec executed no gpgverify call (prep rc 0)) |
| [python-gnupg](python-gnupg/) | PR |  |
| [python-hacking](python-hacking/) | PR |  |
| [python-heatclient](python-heatclient/) | PR |  |
| [python-liblore](python-liblore/) | PR |  |
| [python-libusb1](python-libusb1/) | bug | sha1-cert |
| [python-magnumclient](python-magnumclient/) | PR |  |
| [python-mistralclient](python-mistralclient/) | PR |  |
| [python-neutronclient](python-neutronclient/) | PR |  |
| [python-octaviaclient](python-octaviaclient/) | PR |  |
| [python-osc-lib](python-osc-lib/) | PR |  |
| [python-osc-placement](python-osc-placement/) | PR |  |
| [python-oslo-concurrency](python-oslo-concurrency/) | PR |  |
| [python-oslo-config](python-oslo-config/) | PR |  |
| [python-oslo-context](python-oslo-context/) | PR |  |
| [python-oslo-i18n](python-oslo-i18n/) | PR |  |
| [python-oslo-log](python-oslo-log/) | PR |  |
| [python-oslo-serialization](python-oslo-serialization/) | PR |  |
| [python-oslotest](python-oslotest/) | PR |  |
| [python-oslo-utils](python-oslo-utils/) | PR |  |
| [python-os-service-types](python-os-service-types/) | PR |  |
| [python-patatt](python-patatt/) | PR |  |
| [python-pskc](python-pskc/) | PR |  |
| [python-reno](python-reno/) | PR |  |
| [python-swiftclient](python-swiftclient/) | PR |  |
| [python-tackerclient](python-tackerclient/) | PR |  |
| [python-troveclient](python-troveclient/) | PR |  |
| [python-zaqarclient](python-zaqarclient/) | PR |  |
| [python-zstarfile](python-zstarfile/) | PR |  |
| [qemu-sanity-check](qemu-sanity-check/) | bug | sha1-cert |
| [qgpgme](qgpgme/) | PR |  |
| [rhythmbox-alternative-toolbar](rhythmbox-alternative-toolbar/) | PR |  |
| [rpminspect-data-centos](rpminspect-data-centos/) | PR |  |
| [screenkey](screenkey/) | PR |  |
| secilc | skipped | superseded: converted in dist-git (snapshot 2026-10-26) |
| [serd](serd/) | PR |  |
| [setxkbmap](setxkbmap/) | PR |  |
| [signify](signify/) | bug | weak-key |
| [slurp](slurp/) | draft PR | keyring refresh proposed |
| [sord](sord/) | PR |  |
| [sratom](sratom/) | PR |  |
| [suil](suil/) | PR |  |
| [swaybg](swaybg/) | draft PR | keyring refresh proposed |
| [swayidle](swayidle/) | draft PR | keyring refresh proposed |
| [swaylock](swaylock/) | draft PR | keyring refresh proposed |
| [sysconftool](sysconftool/) | PR |  |
| [tomcli](tomcli/) | PR |  |
| [trojan](trojan/) | PR |  |
| [wlr-randr](wlr-randr/) | draft PR | keyring refresh proposed |
| [xclipboard](xclipboard/) | PR |  |
| [xdg-desktop-portal-wlr](xdg-desktop-portal-wlr/) | draft PR | keyring refresh proposed |
| [xdriinfo](xdriinfo/) | PR |  |
| [xev](xev/) | PR |  |
| [xgamma](xgamma/) | PR |  |
| [xkill](xkill/) | PR |  |
| [xload](xload/) | PR |  |
| [xlogo](xlogo/) | bug | weak-key |
| [xlsclients](xlsclients/) | PR |  |
| [xmag](xmag/) | bug | weak-key |
| [xmodmap](xmodmap/) | PR |  |
| [xorg-x11-drv-amdgpu](xorg-x11-drv-amdgpu/) | bug | expired |
| [xstdcmap](xstdcmap/) | PR |  |
| [xvinfo](xvinfo/) | PR |  |
| [xwd](xwd/) | PR |  |
| [xwininfo](xwininfo/) | PR |  |
| [xwud](xwud/) | PR |  |
| [yambar](yambar/) | PR |  |
| [yascreen](yascreen/) | draft PR | keyring refresh proposed |
| [zix](zix/) | PR |  |
| [0install](0install/) | PR |  |
| [BibTool](BibTool/) | bug | sha1-cert |
| [NetworkManager-strongswan](NetworkManager-strongswan/) | PR |  |
| [SDL3_net](SDL3_net/) | PR |  |
| [ansible-collection-dellemc-openmanage](ansible-collection-dellemc-openmanage/) | PR |  |
| [ansifilter](ansifilter/) | PR |  |
| [anymeal](anymeal/) | PR |  |
| [apache-commons-text](apache-commons-text/) | bug | unparseable-cert |
| [apache-commons-vfs](apache-commons-vfs/) | bug | unparseable-cert |
| [babeltrace](babeltrace/) | bug | sha1-cert |
| [bino](bino/) | PR |  |
| [bmake](bmake/) | bug | sha1-cert |
| [browserpass](browserpass/) | PR |  |
| [compat-gpgme124](compat-gpgme124/) | PR |  |
| [conserver](conserver/) | PR |  |
| [courier-unicode](courier-unicode/) | bug | sha1-cert |
| [cvs](cvs/) | bug | v3-sig |
| [davfs2](davfs2/) | PR |  |
| [dino](dino/) | PR |  |
| [diskimage-builder](diskimage-builder/) | PR |  |
| [disorderfs](disorderfs/) | PR |  |
| [dnssec-trigger](dnssec-trigger/) | bug | sha1-sig |
| [dropbear](dropbear/) | PR |  |
| [eggdrop](eggdrop/) | bug | sha1-cert |
| [exim](exim/) | PR |  |
| [fail2ban](fail2ban/) | bug | sha1-cert |
| [fcft](fcft/) | PR |  |
| [fcitx5-chinese-addons](fcitx5-chinese-addons/) | bug | sha1-cert |
| [fcitx5-table-other](fcitx5-table-other/) | bug | sha1-cert |
| fedrq | skipped | open PR exists: https://src.fedoraproject.org/rpms/fedrq/pull-request/3 |
| [foot](foot/) | PR |  |
| [freetalk](freetalk/) | PR |  |
| [growlight](growlight/) | PR |  |
| [guile-gnutls](guile-gnutls/) | bug | expired |
| [haruna](haruna/) | PR |  |
| [haunt](haunt/) | PR |  |
| [i3](i3/) | bug | expired |
| [iec16022](iec16022/) | bug | sha1-sig |
| [isync](isync/) | bug | expired |
| [jigdo](jigdo/) | PR |  |
| [kuserfeedback](kuserfeedback/) | PR |  |
| [kvantum](kvantum/) | PR |  |
| [libbsd](libbsd/) | PR |  |
| [libchipcard](libchipcard/) | PR |  |
| [libeatmydata](libeatmydata/) | PR |  |
| [libgsasl](libgsasl/) | bug | binding-after-signature |
| [libmd](libmd/) | PR |  |
| [libnice](libnice/) | bug | sha1-sig |
| [lld15](lld15/) | PR |  |
| [lld18](lld18/) | bug | expired |
| [lxi-tools](lxi-tools/) | bug | sha1-cert |
| [maildrop](maildrop/) | bug | sha1-cert |
| [maven-doxia](maven-doxia/) | PR |  |
| [maven-doxia-sitetools](maven-doxia-sitetools/) | PR |  |
| [maven-reporting-impl](maven-reporting-impl/) | bug | expired |
| [mimedefang](mimedefang/) | PR |  |
| [mingw-libidn2](mingw-libidn2/) | bug | expired |
| [mingw-libssh2](mingw-libssh2/) | PR |  |
| [mingw-nettle](mingw-nettle/) | bug | expired |
| [mingw-objfw](mingw-objfw/) | PR |  |
| [mingw-pcre](mingw-pcre/) | bug | sha1-cert |
| [mpd](mpd/) | bug | sha1-cert |
| [mpop](mpop/) | PR |  |
| [msmtp](msmtp/) | PR |  |
| [munin](munin/) | bug | expired |
| [musl](musl/) | bug | sha1-sig |
| [ncmpc](ncmpc/) | bug | sha1-cert |
| [nettle3.10](nettle3.10/) | PR |  |
| [newsboat](newsboat/) | bug | expired |
| [nghttp3](nghttp3/) | bug | sha1-cert |
| [ngtcp2](ngtcp2/) | bug | sha1-cert |
| [nilfs-utils](nilfs-utils/) | PR |  |
| [normalize](normalize/) | bug | v3-sig |
| [ntpsec](ntpsec/) | bug | expired |
| [objfw](objfw/) | PR |  |
| [openbgpd](openbgpd/) | PR |  |
| [openconnect](openconnect/) | bug | sha1-cert |
| [openvpn](openvpn/) | PR |  |
| [paperkey](paperkey/) | bug | sha1-cert |
| [par2cmdline](par2cmdline/) | bug | sha1-cert |
| [parallel](parallel/) | bug | sha1-cert |
| [pari-nflistdata](pari-nflistdata/) | bug | sha1-cert |
| [pdns-recursor](pdns-recursor/) | PR |  |
| [perl-Net-DNS](perl-Net-DNS/) | PR |  |
| [prosody](prosody/) | bug | expired |
| [puppet](puppet/) | PR |  |
| [pv](pv/) | PR |  |
| [python-b4](python-b4/) | PR |  |
| [python-cinderclient](python-cinderclient/) | PR |  |
| [python-glanceclient](python-glanceclient/) | PR |  |
| [python-ironicclient](python-ironicclient/) | PR |  |
| [python-keystoneauth1](python-keystoneauth1/) | PR |  |
| [python-keystoneclient](python-keystoneclient/) | PR |  |
| [python-manilaclient](python-manilaclient/) | PR |  |
| [python-novaclient](python-novaclient/) | PR |  |
| [python-openstackclient](python-openstackclient/) | PR |  |
| [python-pass-import](python-pass-import/) | PR |  |
| [python-stevedore](python-stevedore/) | PR |  |
| [python-sushy](python-sushy/) | PR |  |
| [radsecproxy](radsecproxy/) | PR |  |
| [recutils](recutils/) | bug | sha1-cert |
| [redwax-tool](redwax-tool/) | PR |  |
| [remind](remind/) | PR |  |
| [reprotest](reprotest/) | PR |  |
| [river](river/) | PR |  |
| [river-classic](river-classic/) | PR |  |
| [rpki-client](rpki-client/) | bug | expired |
| [rpminspect](rpminspect/) | PR |  |
| [rush](rush/) | PR |  |
| [rxvt-unicode](rxvt-unicode/) | PR |  |
| [shigofumi](shigofumi/) | PR |  |
| [skribilo](skribilo/) | bug | expired |
| [sngrep](sngrep/) | PR |  |
| [spread-sheet-widget](spread-sheet-widget/) | bug | expired |
| [swappy](swappy/) | PR |  |
| [terminator](terminator/) | PR |  |
| [tio](tio/) | bug | sha1-cert |
| [tlf](tlf/) | bug | weak-key |
| [tmispell-voikko](tmispell-voikko/) | bug | sha1-sig |
| [tnftp](tnftp/) | bug | sha1-sig |
| [trader](trader/) | PR |  |
| [tth](tth/) | PR |  |
| [unrtf](unrtf/) | bug | sha1-sig |
| [volk](volk/) | bug | expired |
| [weechat](weechat/) | bug | sha1-cert |
| [weldr-client](weldr-client/) | PR |  |
| [wl-mirror](wl-mirror/) | PR |  |
| [wlroots](wlroots/) | bug | expired |
| [wlroots0.18](wlroots0.18/) | PR |  |
| [wlroots0.19](wlroots0.19/) | bug | expired |
| [xalan-c](xalan-c/) | PR |  |
| [xcb-imdkit](xcb-imdkit/) | bug | sha1-cert |
| [xcb-util-errors](xcb-util-errors/) | bug | binding-after-signature |
| [xforms](xforms/) | bug | sha1-sig |
