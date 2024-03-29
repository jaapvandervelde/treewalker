# Changelog

## [Unreleased]

Pending changes for unreleased versions: none.

## [0.1.10] - 2023-03-06

### Changed
  - `OSError` now caught as well, error message reported on standard out, to catch WinError 422 

## [0.1.9] - 2022-08-19

### Fixed
  - relax strict dependency on `conffu` to a `>=` dependency

## [0.1.8] - 2022-01-11

### Added
  - add documentation with MkDocs on https://treewalker.readthedocs.io
  - add `--query_nice/-qn` option that allows specifying unit (`bin` or `si`) and precision for calls to nice_size on query fields that start with `'nice_'`
  - add `site` to project cleanup scripts

### Changed
  - no longer add `nice_size` fields in query results after `size` fields; instead, pass any column named `nice_<whatever>` through `nice_size()`
  - make `-qf` select all files, no longer require `-qf %` because `-qf` would default to `True` as the conffu default; same for `-qd`
  - save `start` and `end` in the `runs` table as UTC, previously as local time

### Fixes
  - remove f-strings from some print statements, breaking potential 3.4.4 compatibility
  - remove walrus assignment, breaking potential 3.4.4 compatibility
  - provide a `nice_` column for the `size` column for results from `-qf` and `-qd`, avoid breaking backward compatibility as a result of change in this version
  - `-qo json` now behaves the same as `-qo csv`, provide 'nice' size fields
  - report option mismatches for `rewrite` and `rewrite_admin` correctly, would get caught but then throw exception
  - updated README.md to match up-to-date options, avoiding deprecated options.
  - fixed broken links in documentation and changelog

## [0.1.5] - 2022-01-10

### Fixed
  - re-added the `--path/-p` switch as an alias for `--walk/-w` and updated readme to use `walk`; future versions may break backward compatibility by removing `path` again in a more controlled fashion

## [0.1.4] - 2021-11-17

### Fixed
  - passing a query with an included limit would cause an error as treewalker attempts to set a limit; now the error is caught and the query retries without the set limit - if another error occurs, it is caught and treewalker exits gracefully

## [0.1.3] - 2021-11-16

### Fixed
  - Missing newline in help text

## [0.1.2] - 2021-11-13

### Fixed
  - merging into a recent database would crash trying to recreate a `runs` table 

## [0.1.1] - 2021-11-12

### Fixed
  - running a query would crash if a size column wasn't included in the query result 

## [0.1.0] - 2021-11-11

### Added
  - all query functionality, for file queries, dir queries, file SQL queries, CLI SQL queries and query output formats CSV, JSON and text
  - CLI options `-qd`/`--query_dir`, `-qf`/`--query_file`, `qh`/`--query_help`, `-ql`/`--query_limit`, `-qo`/`--query_output`, `-qc`/`--query_cli`, and `-qs`/`--query_sql`
  - `nice_size` for pretty-printing the 'size' column in a query result

### Changed
  - (BREAKING) the `-o/--output` is now called `-db/--database` to avoid confusion with query output.

## [0.0.12] - 2021-10-21

### Fixed
  - `--help` with version information was broken

## [0.0.11] - 2021-10-04

### Added
  - `runs` table, saving when the run for a certain root folder (parent_dir == -1) started and ended
  - support for `runs` on older tables when modifying or merging

### Fixed
  - `set_host` parameter error, crashing the application when not provided in some cases

## [0.0.10] - 2021-10-02

### Fixed
  - uncaught PermissionError edge cases.

## [0.0.9] - 2021-10-01

### Added
  - set_host function, to update information gathered without administrative shares with host information
```commandline
treewalker --set_host myhostname --output existing.sqlite
```
# Fixed
  - documentation errors

## [0.0.8] - 2021-09-06

### Added
  - list functions allowing quick retrieval of file and directory lists from the database
  - installer build script specific to XP, tested to work with Python 3.4.4, Pyinstaller 3.0, PyPI win32 219 and Conffu 2.2.16 

### Changed
  - (BREAKING) removed `top_match` option, now providing callback for cases where filtering is required
  - (BREAKING) overwriting the database is no longer the default for neither the class nor the CLI entrypoint  
  - integrated options into the database and checking options when reopening a database
  - replaced Python logic with SQLite logic where possible (for much greater performance)
  - `path` option renamed `walk` and paths passed as a default are processed as part of `walk`
  - `no_access` gets cleaned up on remove and correctly merged and re-indexed

## Fixed
  - correctly deal with no commands on command-line for CLI entry point
  - replaced Python 3.4.4 / PyInstaller 3.0 incompatible starred expressed, for XP compatibility

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
[0.1.8]: /../../../tags/0.1.8
[0.1.7]: /../../../tags/0.1.7
[0.1.6]: /../../../tags/0.1.6
[0.1.5]: /../../../tags/0.1.5
[0.1.4]: /../../../tags/0.1.4
[0.1.3]: /../../../tags/0.1.3
[0.1.2]: /../../../tags/0.1.2
[0.1.1]: /../../../tags/0.1.1
[0.1.0]: /../../../tags/0.1.0
[0.0.12]: /../../../tags/0.0.12
[0.0.11]: /../../../tags/0.0.11
[0.0.10]: /../../../tags/0.0.10
[0.0.9]: /../../../tags/0.0.9
[0.0.8]: /../../../tags/0.0.8
[0.0.2]: /../../../tags/0.0.2
[0.0.1]: /../../../tags/0.0.1
