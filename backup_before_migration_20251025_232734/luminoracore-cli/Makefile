# LuminoraCore CLI Makefile

.PHONY: help install install-dev test test-cov lint format clean build upload docs

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package in production mode
	pip install -e .

install-dev:  ## Install the package in development mode with all dependencies
	pip install -e ".[dev]"

test:  ## Run tests
	pytest

test-cov:  ## Run tests with coverage
	pytest --cov=luminoracore_cli --cov-report=html --cov-report=term

lint:  ## Run linting checks
	flake8 luminoracore_cli tests
	mypy luminoracore_cli

format:  ## Format code with black and isort
	black luminoracore_cli tests
	isort luminoracore_cli tests

clean:  ## Clean build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean  ## Build the package
	python -m build

upload: build  ## Upload to PyPI (requires authentication)
	twine upload dist/*

docs:  ## Build documentation
	cd docs && make html

pre-commit:  ## Install pre-commit hooks
	pre-commit install

check: lint test  ## Run all checks (linting and tests)

dev-setup: install-dev pre-commit  ## Set up development environment

# CLI testing commands
test-validate:  ## Test validate command
	python -m luminoracore_cli validate --help

test-compile:  ## Test compile command
	python -m luminoracore_cli compile --help

test-create:  ## Test create command
	python -m luminoracore_cli create --help

test-serve:  ## Test serve command
	python -m luminoracore_cli serve --help

# Development server
serve-dev:  ## Start development server
	python -m luminoracore_cli serve --port 8000 --reload

# Template commands
list-templates:  ## List available templates
	python -m luminoracore_cli create --list-templates

# Cache management
clear-cache:  ## Clear CLI cache
	rm -rf ~/.luminoracore/cache/

# Version management
version:  ## Show current version
	python -c "from luminoracore_cli import __version__; print(__version__)"

bump-version:  ## Bump version (requires version number)
	@read -p "Enter new version: " version; \
	sed -i "s/__version__ = .*/__version__ = \"$$version\"/" luminoracore_cli/__version__.py; \
	sed -i "s/version = .*/version = \"$$version\"/" pyproject.toml
