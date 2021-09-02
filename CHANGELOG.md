# Changelog

## [Unreleased]

No pending changes for unreleased versions.

## [0.0.2] - 2021-09-02

### Fixed
  - Test and logic for remove would incorrectly think folders were subfolders
  - Off-by-one error in merge function would duplicate last directory id from existing database

### Changed
  - Removed f-strings for Python 3.4 support (so tool can run on Windows XP)
  - Removed reliance on Path.resolve() (for XP support)
  - Added options to avoid use of administrative shares (not available on XP)

## [0.0.1] - 2021-08-27

### Added
  - Modified standalone walker project to become treewalker package.

[Unreleased]: /../../../
[0.0.2]: /../../../tags/0.0.2
[0.0.1]: /../../../tags/0.0.1
