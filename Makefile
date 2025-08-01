.PHONY: install
install: ## Install the virtual environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using uv"
	@uv sync

.PHONY: test
test: ## Run tests with coverage
	@echo "🧪 Running tests with coverage"
	@uv run pytest

.PHONY: release
release: ## Create a GitHub release for the current version
	@version=$$(grep -Po '(?<=version = \")([^\"]+)' pyproject.toml); \
	echo "🚀 Creating release for version $$version".; \
	gh release create "$$version" --generate-notes

.PHONY: docs
docs:
	@echo "📖 Building documentation"
	@uv run --group docs sphinx-build docs docs/_build/html -b html -W

.PHONY: help
help:
	@uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_.-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"

.DEFAULT_GOAL := help
