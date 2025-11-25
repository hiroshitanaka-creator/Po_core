.PHONY: install lint format test typecheck help

install:
	python -m pip install --upgrade pip
	pip install -e .[dev]

lint:
	black --check src tests
	isort --check-only src tests
	flake8 src tests

format:
	black src tests
	isort src tests

typecheck:
	mypy src tests

test:
	pytest

help:
	@echo "Available targets: install, lint, format, typecheck, test"
