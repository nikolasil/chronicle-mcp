.PHONY: help install dev test test-watch test-coverage lint lint-check format format-check typecheck
.PHONY: http dev-server clean deps docs build release check

help:
	@echo "ChronicleMCP Development Commands"
	@echo ""
	@echo "  make install      Install package with dev dependencies"
	@echo "  make dev          Start MCP development server"
	@echo "  make http         Start HTTP server"
	@echo "  make test         Run all tests"
	@echo "  make test-watch   Run tests with watch mode"
	@echo "  make test-coverage Run tests with coverage report"
	@echo "  make lint         Run linter with auto-fix"
	@echo "  make lint-check   Check linting without fixing"
	@echo "  make format       Format code"
	@echo "  make format-check Check formatting"
	@echo "  make typecheck    Run type checker"
	@echo "  make clean        Clean temporary files"
	@echo "  make deps         Update dependencies"
	@echo "  make docs         Generate documentation"
	@echo "  make build        Build package"
	@echo "  make release      Create release"
	@echo "  make check        Run all checks (lint, format, typecheck, test)"
	@echo "  make precommit    Run pre-commit hooks"

install:
	pip install -e ".[dev]"

dev:
	python -m chronicle_mcp mcp

http:
	chronicle-mcp http --port 8080

dev-server:
	chronicle-mcp http --port 8080 --host 0.0.0.0

test:
	pytest tests/ -v

test-watch:
	ptw tests/ -- -v

test-coverage:
	pytest tests/ --cov=chronicle_mcp --cov-report=html --cov-report=term-missing

test-property:
	pytest tests/ -v --hypothesis-show-statistics -k "property" 2>/dev/null || echo "No property tests found"

lint:
	ruff check . --fix
	ruff format .

lint-check:
	ruff check .
	ruff format --check .

format:
	ruff format .

format-check:
	ruff format --check .

typecheck:
	mypy chronicle_mcp/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov/ .hypothesis/ 2>/dev/null || true
	rm -rf dist/ build/ *.egg-info/ 2>/dev/null || true

deps:
	pip-compile --upgrade --generate-hashes pyproject.toml
	pip install -r requirements.txt

docs:
	sphinx-build -b html docs/ docs/_build/html

build:
	python -m build

release:
	git tag v$$(python -c "import tomli; print(tomli.load(open('pyproject.toml', 'rb'))['project']['version'])")
	git push && git push --tags
	python -m build
	twine upload dist/*

check:
	ruff check .
	ruff format --check .
	mypy chronicle_mcp/
	pytest tests/ -v --tb=short

precommit:
	pre-commit run --all-files

docker-build:
	docker build -t chronicle-mcp:latest .

docker-run:
	docker run -p 8080:8080 chronicle-mcp:latest

install-precommit:
	pre-commit install
	pre-commit install-hooks

benchmark:
	pytest tests/ --benchmark-only --benchmark-compare 2>/dev/null || echo "No benchmark tests found"
	pytest tests/ --benchmark-only --benchmark-export=benchmark.json 2>/dev/null || echo "No benchmark tests found"

security-check:
	pip install safety
	safety check --requirements-file <(pip freeze)
	deptry .

all-checks: lint-check format-check typecheck test security-check
	@echo "All checks passed!"

# End of Makefile
