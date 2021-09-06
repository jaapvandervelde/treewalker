# Changelog

## [Unreleased]

No pending changes for unreleased versions.

## [0.0.3] - 2021-09-06

### Added
  - list functions allowing quick retrieval of file and directory lists from the database

### Changed
  - (BREAKING) removed `top_match` option, now providing callback for cases where filtering is required
  - integrated options into the database and checking options when reopening a database
  - replaced Python logic with SQLite logic where possible (for much greater performance)

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
[0.0.3]: /../../../tags/0.0.3
[0.0.2]: /../../../tags/0.0.2
[0.0.1]: /../../../tags/0.0.1
