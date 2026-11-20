# rpm: verify source signatures with openpgpverify

Fedora is moving source signature checks from `%gpgverify` (GnuPG) to
`%openpgpverify` (Sequoia sqv) as part of the approved Change
https://fedoraproject.org/wiki/Changes/Sequoia_openpgpverify. sqv follows
the system crypto policy, checks that the key was valid when the release
was signed, and supports the current OpenPGP standard (RFC 9580).

The change was merged in Fedora dist-git
(https://src.fedoraproject.org/rpms/crun/pull-request/159), but the Packit
sync of 1.31 replaced the spec with this one, so it belongs here.

- Fedora and RHEL 11 (ELN): `%openpgpverify`, `BuildRequires: openpgpverify`
- RHEL 10 and older (CentOS Stream): unchanged, `%gpgverify` and
  `BuildRequires: gnupg2`, since openpgpverify is not available there
- COPR builds: no check, as before

Checked with `rpmspec -P` for each case; sqv accepts `crun.keyring` for
the 1.31 release.
