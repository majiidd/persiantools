# Changelog

## [6.1.0](https://github.com/majiidd/persiantools/compare/6.0.2...6.1.0) - 2026-07-10

- Added the `convert-persian-dates` AI agent skill (`.agents/skills/convert-persian-dates/`) so AI coding assistants can convert Shamsi/Jalali and Gregorian dates without guessing calendar math.
- Documented the skill in `README.md`, including installation via `npx skills add`.
- Pointed `CLAUDE.md` at `AGENTS.md` so Claude picks up the existing agent workflow instructions.

## [6.0.2](https://github.com/majiidd/persiantools/compare/6.0.1...6.0.2) - 2026-07-10

- Added performance regression coverage for Jalali/Gregorian date conversion.
- Refreshed package metadata and documented the contributor and agent development workflow.

## [6.0.1](https://github.com/majiidd/persiantools/compare/6.0.0...6.0.1) - 2026-07-10

- Hardened GitHub Actions workflow permissions (`contents: read` at workflow and publish-job level).
- Bumped `astral-sh/setup-uv` to v8.3.2.
- Switched the Black pre-commit hook to `psf/black-pre-commit-mirror`.
- Expanded pre-commit checks (`check-docstring-first`, additional `pygrep-hooks`, `validate-pyproject`) and bumped mypy to v2.2.0.
- Refreshed locked transitive dependencies (`filelock`, `virtualenv`, `python-discovery`).

## [6.0.0](https://github.com/majiidd/persiantools/compare/5.5.1...6.0.0) - 2026-07-03

Performance:

- Rewrote the core `JalaliDate.to_jalali()` and `JalaliDate.to_gregorian()` conversion methods for performance and readability.

Brought `JalaliDate`/`JalaliDateTime` to feature parity with the `datetime` API as of Python 3.14:

- Added `fold` support (PEP 495) to `JalaliDateTime`: keyword-only constructor argument, `fold` property, propagation through `replace()`, `to_gregorian()`/`to_jalali()`, `combine()`, `time()`/`timetz()`, pickling, `repr()`, and fold-aware equality/hashing for ambiguous wall times.
- Added `timespec` argument to `JalaliDateTime.isoformat()` (`auto`, `hours`, `minutes`, `seconds`, `milliseconds`, `microseconds`).
- Added `fromisocalendar()` to `JalaliDate` and `JalaliDateTime`, the inverse of `isocalendar()`.
- `isocalendar()` now returns a named tuple with `year`, `week`, and `weekday` fields (still compares equal to the old plain tuple).
- Expanded `fromisoformat()` to accept the basic format `YYYYMMDD` and week dates `YYYY-Www[-D]` / `YYYYWww[d]` (Python 3.11 parity).
- Added the `%:z` strftime directive (UTC offset with a colon, Python 3.12 parity).
- Added `copy.replace()` support via `__replace__` on both classes (Python 3.13 parity).
- Added `%j`, `%w`, `%U`, and `%W` directives to `strptime()` on both classes.
- Added `min`/`max` class attributes; fixed `JalaliDateTime.resolution` (now `timedelta(microseconds=1)`).
- Deprecated `JalaliDateTime.utcnow()` and `JalaliDateTime.utcfromtimestamp()` (mirroring Python 3.12); use `now(timezone.utc)` and `fromtimestamp(t, tz=timezone.utc)`.
- Fixed `JalaliDateTime.fromordinal()`/`to_jalali()` crashing when time components were omitted.

Tooling:

- Migrated development and CI tooling from `pipenv` to [uv](https://docs.astral.sh/uv/); dev dependencies now live in the `[dependency-groups]` table of `pyproject.toml` with a committed `uv.lock`. The published package is unchanged.
- Added `Makefile`, and Dependabot updates for the `uv` and `github-actions` ecosystems.

## [5.5.1](https://github.com/majiidd/persiantools/compare/5.5.0...5.5.1) - 2026-05-05

- Fixed `JalaliDateTime` copy-constructor to preserve `tzinfo` when initialized from another timezone-aware `JalaliDateTime` (fixes [#62](https://github.com/majiidd/persiantools/issues/62)).
- Added regression coverage for timezone-preserving constructor behavior and explicit `tzinfo` override semantics.
- This bug fix was implemented with Cursor AI assistance.

## [5.5.0](https://github.com/majiidd/persiantools/compare/5.4.0...5.5.0) - 2026-01-30

- Python 3.14 support.
- Migrated from `setup.py` to `pyproject.toml` (PEP 621).
- Improved CI/CD pipeline with job dependencies and parallel execution.
- Marked Python 3.15 as experimental with allowed failures.

## [5.4.0](https://github.com/majiidd/persiantools/compare/5.3.0...5.4.0) - 2025-09-26

- Removed `pytz` dependency; migrated fully to `zoneinfo` and `datetime.timezone`.
- Updated `JalaliDateTime` implementation and fixed timezone handling.
- Refined CI/CD workflows and linting configuration.

## [5.3.0](https://github.com/majiidd/persiantools/compare/5.2.1...5.3.0) - 2025-06-06

- Added `strptime` support to `JalaliDate` for parsing date strings.

## [5.2.1](https://github.com/majiidd/persiantools/compare/5.2.0...5.2.1) - 2025-06-06

- Added a Support section to the README.
- Added a lint step to the CI/CD pipeline.
- Updated dependencies to the latest versions.
- Added PyPy 3.11 to GitHub Workflows test matrix.
- Fixed Python version mismatch in CI workflows.
- Enhanced README with comprehensive usage examples.

## [5.2.0](https://github.com/majiidd/persiantools/compare/5.1.1...5.2.0) - 2025-01-17

- Enhanced character conversion functions using regular expressions.
- Improved date handling in Jalali date and time classes.
- Added new test cases for edge cases and date conversions.

## [5.1.1](https://github.com/majiidd/persiantools/compare/5.1.0...5.1.1) - 2025-01-16

- Improved leap year calculation for issue #48.

## [5.1.0](https://github.com/majiidd/persiantools/compare/5.0.0...5.1.0) - 2024-11-08

- Improved CI/CD pipeline run time through optimized caching.

## [5.0.0](https://github.com/majiidd/persiantools/compare/4.2.0...5.0.0) - 2024-11-08

- Dropped Python 3.8 support; added Python 3.13 compatibility.
- Added type annotations to methods.
- Expanded test suite with new tests.
- Updated dependencies to the latest versions.

## [4.2.0](https://github.com/majiidd/persiantools/compare/4.1.2...4.2.0) - 2024-06-28

- Added `CHANGELOG.md` to track changes in the project.

## [4.1.2](https://github.com/majiidd/persiantools/compare/4.1.1...4.1.2) - 2024-06-28

- Added `fromisoformat` method for `JalaliDateTime`.

## [4.1.1](https://github.com/majiidd/persiantools/compare/4.1.0...4.1.1) - 2024-06-28

- Fixed the `strftime` method to handle timezone correctly and added comprehensive tests.

## [4.1.0](https://github.com/majiidd/persiantools/compare/4.0.3...4.1.0) - 2024-06-28

- Add comprehensive tests and docstrings
- Refactor `JalaliDate` methods and fix issues
- Update `.gitignore` and fix type annotations

## [4.0.3](https://github.com/majiidd/persiantools/compare/4.0.2...4.0.3) - 2024-06-23

- Fixed the leap year calculation in the `to_jalali` function.

## [4.0.2](https://github.com/majiidd/persiantools/compare/4.0.1...4.0.2) - 2024-05-12

- Fixed a bug with the first day of the year.

## [4.0.1](https://github.com/majiidd/persiantools/compare/4.0.0...4.0.1) - 2024-05-12

- Upgraded dependencies.

## [4.0.0](https://github.com/majiidd/persiantools/compare/v3.0.1...4.0.0) - 2024-03-24

- Fixed comparison operations.
- Corrected function name from `chack_date` to `check_date`.
- Updated various configurations and dependencies.

## [v3.0.1](https://github.com/majiidd/persiantools/compare/v3.0.0...v3.0.1) - 2022-05-14

- Fixed timezone handling in datetime parsing.
- Updated pre-commit configuration.
- Fixed minor issues in comparisons.

## [v3.0.0](https://github.com/majiidd/persiantools/compare/v2.4.1...v3.0.0) - 2022-03-11

- Added Python 3.10 support in setup classifiers.
- Removed `.travis.yml`.
- Fixed comparisons to always return a boolean.

## [v2.4.1](https://github.com/majiidd/persiantools/compare/v2.3.2...v2.4.1) - 2022-03-11

- Added float number to word conversion.
- Fixed issues with negative numbers and floating point numbers.

## [v2.3.2](https://github.com/majiidd/persiantools/compare/v2.3.1...v2.3.2) - 2022-03-11

- Improved handling of leap years in date calculations.

## [v2.3.1](https://github.com/majiidd/persiantools/compare/v2.3.0...v2.3.1) - 2022-03-10

- Fixed date parsing issues.

## [v2.3.0](https://github.com/majiidd/persiantools/compare/v2.2.0...v2.3.0) - 2022-03-10

- Improved Python 3.10 compatibility.
- Fixed various issues in date handling.

## [v2.2.0](https://github.com/majiidd/persiantools/compare/v2.1.2...v2.2.0) - 2021-11-19

- Implemented `strptime` for `JalaliDateTime`.
- Improved handling of timezones.

## [v2.1.2](https://github.com/majiidd/persiantools/compare/v2.1.1...v2.1.2) - 2021-07-16

- Fixed datetime formatting issues.
- Improved locale handling in date conversions.

## [v2.1.1](https://github.com/majiidd/persiantools/compare/v2.1.0...v2.1.1) - 2021-03-05

- Improved handling of Persian digits in date parsing.

## [v2.1.0](https://github.com/majiidd/persiantools/compare/v2.0.0...v2.1.0) - 2021-03-05

- Added number to letter conversion feature.
- Improved datetime parsing and formatting.

## [v2.0.0](https://github.com/majiidd/persiantools/compare/v1.5.1...v2.0.0) - 2021-02-11

- Added support for datetime parsing and formatting.
- Improved handling of different locales.

## [v1.5.1](https://github.com/majiidd/persiantools/compare/v1.5.0...v1.5.1) - 2020-10-28

- Removed `check_int_field`.
- Updated CI configuration.

## [v1.5.0](https://github.com/majiidd/persiantools/compare/v1.4.0...v1.5.0) - 2020-07-27

- Added support for Unicode type (Python 2) to converter methods.
- Added examples and tests.
- Added support for Python 2.7 and PyPy.
- Added `JalaliDateTime` converter and tests.
- Added character converter to Persian.
- Applied Black formatter.
- Fixed various bugs.
- Changed repository and project configuration.
