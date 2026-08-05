# AGENTS.md

Development guide for AI coding agents and contributors working on
`persiantools`.

This file is for repository work: setup, coding, tests, reviews, releases, and
maintenance. End-user installation and usage examples belong in [README.md](README.md).

When this guide and tool output disagree, the repository configuration is the
source of truth: [pyproject.toml](pyproject.toml), [Makefile](Makefile),
[.pre-commit-config.yaml](.pre-commit-config.yaml), [.flake8](.flake8), and
[.github/workflows/ci.yml](.github/workflows/ci.yml).

## Scope and Precedence

- This root `AGENTS.md` applies to the whole repository.
- Direct maintainer or user instructions in the current task override this file.
- Keep this file agent-focused. Put human-facing project narrative in
  `README.md` and release history in `CHANGELOG.md`.

## Project Snapshot

- `persiantools` is a pure-Python, MIT-licensed package for Jalali (Shamsi)
  dates/datetimes and Persian text utilities.
- Runtime dependencies must stay at zero except for the current Windows-only
  `tzdata` dependency.
- Supported runtimes are CPython 3.9 through 3.14 and PyPy. CI also runs an
  experimental CPython 3.15 job on Linux.
- Code must remain Python 3.9-compatible. Pre-commit enforces this with
  `pyupgrade --py39-plus`.
- The default branch is `master`; releases are published from bare version tags
  such as `6.0.1`.

## Repository Map

| Path | Purpose |
| --- | --- |
| `persiantools/` | Library source code. Public package metadata and `__version__` live in `persiantools/__init__.py`. |
| `persiantools/jdatetime.py` | `JalaliDate` and `JalaliDateTime`, including conversion, parsing, formatting, arithmetic, and timezone behavior. |
| `persiantools/digits.py` | Digit conversion and Persian number-to-word helpers. |
| `persiantools/characters.py` | Arabic/Persian character normalization helpers. |
| `persiantools/utils.py` | Shared validation and conversion helpers. |
| `tests/` | Pytest suite. Test files are named `test_*.py`. |
| `README.md` | End-user documentation and examples. |
| `CHANGELOG.md` | Human-written release notes. |
| `pyproject.toml` | Project metadata, dependency groups, build backend, and tool configuration. |
| `uv.lock` | Locked development dependencies. Regenerate with `make lock`; do not hand-edit. |
| `Makefile` | Canonical development commands. |
| `.pre-commit-config.yaml` | Format, lint, type, security, and metadata validation hooks. |
| `.flake8` | Flake8 configuration kept compatible with Black. |
| `.github/workflows/ci.yml` | CI, build, Test PyPI, and PyPI publishing workflow. |

## Environment

Use `uv` 0.11.0 or newer. For a fresh checkout:

```bash
make install
```

This runs `uv sync --locked` and installs the pre-commit hooks.

Common commands:

| Command | Use |
| --- | --- |
| `make` | Show all documented Make targets. |
| `make sync` | Create or update the local environment from `uv.lock`. |
| `make hooks` | Install pre-commit hooks. |
| `make test` | Run the full test suite. |
| `make cov` | Run tests with terminal coverage details. |
| `make lint` | Run all pre-commit hooks on all files. |
| `make format` | Run isort and Black through pre-commit. |
| `make check` | Run lint and tests, matching the main local CI gate. |
| `make build` | Build the sdist and wheel. |
| `make lock` | Refresh `uv.lock` after dependency metadata changes. |
| `make upgrade` | Upgrade locked dependencies within configured version bounds. |
| `make clean` | Remove local build, cache, and coverage artifacts. |

Useful focused commands:

```bash
uv run --no-sync pytest -ra tests/test_digits.py
uv run --no-sync pytest -ra tests/test_jalalidate.py -k fromisoformat
uv run --no-sync pre-commit run black --files persiantools/jdatetime.py
uv run --no-sync pre-commit run mypy --all-files
```

Prefer `make` targets for final validation because they match the repository's
documented workflow.

## Agent Workflow

1. Start by checking the working tree with `git status --short`.
2. Read the relevant source, tests, and config before editing. Prefer `rg` for
   searches.
3. Preserve unrelated user changes. Do not revert, restage, or clean files you
   did not intentionally modify.
4. Make the smallest coherent change that fixes the issue or implements the
   request.
5. Add or update tests for every behavior change.
6. Update docs only when user-visible behavior, examples, requirements, or
   development workflow changes.
7. Run the narrowest useful test during iteration, then run `make check` before
   finishing when practical.
8. If a required check cannot run locally, report the command and the reason.

## Coding Standards

- Use Black and isort with a 120-character line length.
- Keep public APIs type-annotated and documented with docstrings.
- Match the standard-library `datetime` API where `JalaliDate` or
  `JalaliDateTime` mirrors a `date` or `datetime` behavior.
- Prefer clear, small functions over broad rewrites. Avoid unrelated refactors.
- Keep code compatible with Python 3.9 and PyPy.
- Use only the standard library at runtime unless a maintainer explicitly agrees
  to a dependency change.
- Do not use `eval`.
- Do not add blanket `# noqa` or blanket `# type: ignore` comments.
- Avoid global mutable state and hidden environment-dependent behavior.
- Files must use LF line endings and end with a newline.
- Consider performance.

## Library Behavior Notes

- Preserve backward-compatible behavior unless the task is explicitly a breaking
  change.
- Be careful with Jalali/Gregorian conversion edge cases: Norouz boundaries,
  Esfand 29/30, Gregorian century leap-year boundaries, min/max supported years,
  and timestamp/from-ordinal behavior.
- The calendar model is layered (astronomical leap data for years 1-1177, the
  33-year rule plus the ICU4X correction set for 1178-2987, the plain 33-year
  rule beyond); see the README "Calendar model" section. Keep every conversion
  derived from `_days_before_year`/`is_leap` in `persiantools/jdatetime.py` --
  never reintroduce independent conversion arithmetic.
- Timezone behavior should use `zoneinfo`, `datetime.timezone`, and the stdlib
  `datetime` model. Do not reintroduce `pytz`.
- Locale-sensitive behavior currently uses `"en"` and `"fa"`. Keep Persian digit
  and character normalization behavior explicit in tests.
- Public examples in `README.md` should stay runnable and consistent with the
  current API.

## Testing Guidance

- Put tests in `tests/` using the existing `test_*.py` naming pattern.
- Existing tests mix `unittest.TestCase` and pytest helpers; follow nearby style.
- Use table-driven tests for calendar conversion cases and parsing/formatting
  variants.
- Bug fixes should include a regression test. Reference the issue number in the
  test name, comment, or changelog entry when there is a public issue.
- Cover both success and failure paths for validation, parsing, locale, and type
  errors.
- For date/time changes, include timezone-aware and timezone-naive cases when
  relevant.
- Coverage should not decrease. Use `make cov` when a change is broad or subtle.

## Dependency Policy

- Runtime dependencies belong in `[project].dependencies` and should remain
  empty except for `tzdata; platform_system == 'Windows'`.
- Development dependencies belong in `[dependency-groups].dev`.
- After dependency metadata changes, run `make lock`.
- Never hand-edit `uv.lock`.
- Do not vendor third-party code into the repository without maintainer approval
  and clear license notes.

## Documentation Policy

- Update `README.md` for user-facing API changes, changed requirements, or new
  examples.
- Update `AGENTS.md` when development commands, CI requirements, or agent
  workflow expectations change.
- Update `CHANGELOG.md` only when preparing a release or when a maintainer asks
  for a changelog entry.
- Keep documentation concise, accurate, and linked to the relevant source files
  or commands.

## Security and Supply Chain

- Do not commit secrets, tokens, credentials, private keys, or local `.env`
  values.
- Do not weaken GitHub Actions permissions or publishing safeguards.
- Keep the trusted-publishing release flow intact; do not add manual package
  upload steps.
- Treat parsing, formatting, and Unicode normalization changes as security
  sensitive when they could affect validation or user data.
- Bandit runs in pre-commit. Investigate findings instead of suppressing them
  broadly.

## Git and PR Workflow

- Do not commit directly to `master`.
- Use small, single-purpose branches with descriptive prefixes such as
  `feature/`, `fix/`, or `ci/`.
- Commit messages should be imperative and concise. Reference issues as `#NN`
  when relevant.
- Pull requests are squash-merged into `master`, so keep the PR title and body
  suitable for a final squash commit.
- CI must be green before merge: lint, full test matrix, build, and package
  metadata checks.

## Release Workflow

Do not bump versions, create tags, or publish releases unless explicitly asked by
a maintainer.

Release checklist:

1. Bump `__version__` in `persiantools/__init__.py`.
2. Add a dated compare-link entry to `CHANGELOG.md` following the existing
   format.
3. Open a release PR and squash-merge it into `master`.
4. Tag `master` with the bare version `X.Y.Z` without a `v` prefix.
5. Push the tag. CI builds artifacts, publishes to Test PyPI, then publishes to
   PyPI through trusted publishing.

## Files and Paths to Avoid

- Do not edit generated or local artifact paths unless the task explicitly
  requires it: `dist/`, `build/`, `*.egg-info/`, `.venv/`, `.pytest_cache/`,
  `.mypy_cache/`, `.ruff_cache/`, `htmlcov/`, and coverage files.
- Do not commit local IDE files, operating-system files, or environment files.
- Do not modify `uv.lock` manually; use `make lock`.
- Do not make sweeping formatting changes outside the files touched by the task
  unless the task is specifically formatting-related.

## Before Finishing

- Confirm the diff only contains intended changes.
- Run relevant targeted tests.
- Run `make check` when practical.
- Summarize what changed, which checks ran, and any remaining risk or skipped
  validation.
