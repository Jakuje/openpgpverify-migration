# Drop BuildRequires: gnupg2

The source signature check was removed in 48e8933 (rhbz#2571543), but
`BuildRequires: gnupg2` stayed. Nothing else in the build uses GnuPG, so it
can go.

This also takes dhcp off the list of packages that require GnuPG to build,
which matters for ELN: as part of
https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify, ELN packages
are moving away from GnuPG-based source verification
(https://github.com/fedora-eln/eln/issues/610).

Tested with a full build (`rpmbuild -bb`) in mock for Fedora rawhide and ELN,
with all `gnupg2*` packages removed from the buildroot (gnupg2 is otherwise
present in every buildroot, so a normal build would not show a hidden
dependency). The build log shows no GnuPG use. The spec uses
`%autorelease`/`%autochangelog`, so the commit message is the changelog entry.
