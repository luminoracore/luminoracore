.PHONY: help install install-dev test lint format clean build dist upload docs

help:
	@echo "LuminoraCore Development Commands:"
	@echo ""
	@echo "  install      Install the package in development mode"
	@echo "  install-dev  Install with development dependencies"
	@echo "  test         Run all tests"
	@echo "  lint         Run linting checks"
	@echo "  format       Format code with black"
	@echo "  clean        Clean build artifacts"
	@echo "  build        Build the package"
	@echo "  dist         Create distribution packages"
	@echo "  upload       Upload to PyPI (requires credentials)"
	@echo "  docs         Generate documentation"
	@echo "  validate     Validate all personalities"
	@echo "  compile      Test compilation for all providers"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=luminoracore --cov-report=html --cov-report=term-missing

lint:
	flake8 luminoracore/ tests/ examples/
	mypy luminoracore/

format:
	black luminoracore/ tests/ examples/
	isort luminoracore/ tests/ examples/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

dist: build

upload: dist
	twine upload dist/*

docs:
	@echo "Documentation generation not implemented yet"

validate:
	python -m luminoracore.tools.validator --all

compile:
	python -m luminoracore.tools.compiler --test-all

# Development shortcuts
dev: install-dev
	@echo "Development environment ready!"

quick-test:
	pytest tests/ -v

quick-lint:
	flake8 luminoracore/
