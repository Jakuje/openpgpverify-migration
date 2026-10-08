# Phase 1 results

Generated 2026-10-08T12:11Z from `data/state/packages.jsonl`: 19 of 594 packages tested.

| Status | Packages |
|---|---|
| `tested` | 10 |
| `regression` | 7 |
| `manual` | 2 |

| Regression reason | Calls |
|---|---|
| `sha1-cert` | 4 |
| `sha1-sig` | 1 |
| `v3-sig` | 1 |
| `expired` | 1 |

| Package | Status | Calls old→new | Chroots | Notes |
|---|---|---|---|---|
| gnupg2 | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libgpg-error | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libksba | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| libssh | `tested` | 1→1 | rawhide: both-pass | BR gnupg2 kept (review) |
| openssl-pkcs11 | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| pinentry | `tested` | 1→1 | rawhide: both-pass |  |
| yubikey-manager-qt | `regression` | 1→1 | rawhide: regression | reason: expired; keyring refresh: proposed |
| openssh | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| pcsc-lite-ccid | `manual` | 1→0 | rawhide: manual | raw verification baseline passes |
| wob | `tested` | 1→1 | rawhide: both-pass |  |
| getdns | `regression` | 1→1 | rawhide: regression | BR gnupg2 kept (review); reason: sha1-cert; keyring refresh: no-update |
| python-ezgb | `tested` | 1→1 | rawhide: both-pass |  |
| dns-root-data | `regression` | 1→1 | rawhide: regression | reason: sha1-sig |
| libstrophe | `tested` | 1→1 | rawhide: both-pass |  |
| openresolv | `regression` | 1→1 | rawhide: regression | rhel conditional: use the README template for the PR; reason: sha1-cert; keyring refresh: proposed |
| fapolicyd | `tested` | 2→2 | rawhide: both-pass, eln: not-buildable | unchanged spec: installdeps failed; dropped conditional BR: BuildRequires: gpgverify; rhel conditional: use t… |
| python-oslo-metrics | `tested` | 1→1 | rawhide: both-pass | dropped conditional BR: BuildRequires:  /usr/bin/gpgv2 |
| mpdscribble | `regression` | 1→1 | rawhide: regression | reason: sha1-cert; keyring refresh: no-update |
| rsakeyfind | `regression` | 1→1 | rawhide: regression | reason: v3-sig |
