.PHONY: install install-dev format lint typecheck test coverage security docs help

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

format:
	black src tests
	isort src tests

lint:
	flake8 src tests
	pylint src tests

typecheck:
	mypy src tests

test:
	pytest

coverage:
	pytest --cov=po_core --cov-report=term-missing

security:
	bandit -r src
	safety check -r requirements.txt

docs:
	sphinx-build -b html docs docs/_build/html

help:
	@echo "Available commands:"
	@echo "  make install       Install production dependencies"
	@echo "  make install-dev   Install development dependencies"
	@echo "  make format        Run black and isort"
	@echo "  make lint          Run flake8 and pylint"
	@echo "  make typecheck     Run mypy"
	@echo "  make test          Run pytest"
	@echo "  make coverage      Run pytest with coverage output"
	@echo "  make security      Run bandit and safety checks"
	@echo "  make docs          Build Sphinx documentation"
