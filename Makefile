.DEFAULT_GOAL := help

.PHONY: help install dev test lint format run

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install -e .

dev: ## Install with dev dependencies and set up pre-commit hooks
	pip install -e '.[dev]'
	pip install pre-commit
	pre-commit install

test: ## Run the test suite with pytest
	pytest

lint: ## Run ruff linter checks
	ruff check .

format: ## Auto-format code with ruff
	ruff format .

run: ## Start the development server (uses run.sh)
	bash run.sh
