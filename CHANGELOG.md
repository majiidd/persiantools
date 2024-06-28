
# Changelog

## [4.2.0](https://github.com/majiidd/persiantools/compare/4.1.2...4.2.0) (2024-06-28)

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
