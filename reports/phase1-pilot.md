# Phase 1 results

Generated 2026-10-09T13:20Z from `data/state/packages.jsonl`: 35 of 594 packages tested.

| Status | Packages |
|---|---|
| `tested` | 24 |
| `regression` | 8 |
| `manual` | 2 |
| `superseded` | 1 |

| Regression reason | Calls |
|---|---|
| `sha1-cert` | 5 |
| `sha1-sig` | 1 |
| `v3-sig` | 1 |
| `binding-after-signature` | 1 |
| `expired` | 1 |

| Package | Status | Calls old→new | Chroots | Notes |
|---|---|---|---|---|
| gnupg2 | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libgpg-error | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libksba | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libssh | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| openssl-pkcs11 | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| pinentry | `tested` | 1→1 | rawhide: both-pass, eln: both-pass |  |
| yubikey-manager-qt | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| openssh | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| pcsc-lite-ccid | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| wob | `tested` | 1→1 | rawhide: both-pass |  |
| getdns | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: no-update |
| python-ezgb | `tested` | 1→1 | rawhide: both-pass |  |
| dns-root-data | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| libstrophe | `tested` | 1→1 | rawhide: both-pass |  |
| openresolv | `regression` | 1→1 | rawhide: regression, eln: regression | rhel conditional: gpgverify kept for RHEL < 11 / EPEL; reason: sha1-cert; reason: sha1-cert; keyring refresh:… |
| fapolicyd | `tested` | 2→2 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; replaced conditional BR in place: BuildRequires: gpgverify; rhel conditio… |
| python-oslo-metrics | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| mpdscribble | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| rsakeyfind | `regression` | 1→1 | rawhide: regression | reason: v3-sig |
| vali | `tested` | 1→1 | rawhide: both-pass |  |
| mooltipass-udev | `tested` | 1→1 | rawhide: both-pass |  |
| basez | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| hiera | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| kio-fuse | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| i3status | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| conflict | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| ssh-audit | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| logrotate | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| vim-latex | `tested` | 1→1 | rawhide: both-pass |  |
| libmnl | `tested` | 1→1 | rawhide: both-pass |  |
| time | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: binding-after-signature; keyring refresh: proposed |
| dbus-glib | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| gnulib-l10n | `tested` | 1→1 | rawhide: both-pass |  |
| radvd | `superseded` | -→- |  |  |
| dbus | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
