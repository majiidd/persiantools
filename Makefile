.DEFAULT_GOAL := help
.PHONY: help install sync hooks test cov lint format build check lock upgrade clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

install: sync hooks ## Set up the full dev environment (sync + git hooks)

sync: ## Create the venv and install locked dependencies
	uv sync --locked

hooks: ## Install the pre-commit git hooks
	uv run pre-commit install

test: ## Run the test suite
	uv run --no-sync pytest -ra tests/

cov: ## Run the test suite with a coverage report
	uv run --no-sync pytest -ra --cov=persiantools --cov-report=term-missing tests/

lint: ## Run all pre-commit checks on all files
	uv run --no-sync pre-commit run --all-files

format: ## Auto-format the code (isort + black via pre-commit)
	uv run --no-sync pre-commit run isort --all-files
	uv run --no-sync pre-commit run black --all-files

check: lint test ## Run lint and tests (what CI enforces)

build: ## Build the sdist and wheel
	uv build

lock: ## Refresh uv.lock from pyproject.toml
	uv lock

upgrade: ## Upgrade all locked dependencies to their latest allowed versions
	uv lock --upgrade

clean: ## Remove build artifacts and caches
	rm -rf build/ dist/ *.egg-info persiantools.egg-info \
		.pytest_cache .mypy_cache .ruff_cache .coverage coverage.xml htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
