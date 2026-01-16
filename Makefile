.PHONY: install dev test lint format build-lambda deploy-backend fetch help

# Default target
help:
	@echo "Stonksfeed.com Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install        Install all dependencies"
	@echo "  make dev            Install with dev dependencies"
	@echo ""
	@echo "Python Development (packages/stonksfeed):"
	@echo "  make test           Run Python tests"
	@echo "  make lint           Run linters"
	@echo "  make format         Format code"
	@echo "  make fetch          Fetch articles locally"
	@echo "  make fetch-json     Fetch articles as JSON"
	@echo ""
	@echo "Lambda Packaging:"
	@echo "  make build-lambda   Package stonksfeed for Lambda"
	@echo ""
	@echo "Frontend:"
	@echo "  make frontend-dev   Start frontend dev server"
	@echo "  make frontend-build Build frontend for production"
	@echo ""

# Install all dependencies
install:
	cd packages/stonksfeed && uv sync
	cd frontend && npm ci
	cd infrastructure && uv sync

# Install with dev dependencies
dev:
	cd packages/stonksfeed && uv sync --all-extras
	cd frontend && npm ci
	cd infrastructure && uv sync

# Run Python tests
test:
	cd packages/stonksfeed && uv run pytest tests/ -v

# Run Python tests with coverage
coverage:
	cd packages/stonksfeed && uv run pytest tests/ -v --cov=stonksfeed --cov-report=term-missing

# Lint Python code
lint:
	cd packages/stonksfeed && uv run ruff check src/ tests/

# Format Python code
format:
	cd packages/stonksfeed && uv run ruff format src/ tests/
	cd packages/stonksfeed && uv run ruff check --fix src/ tests/

# Fetch articles locally (for testing scrapers)
fetch:
	cd packages/stonksfeed && uv run stonksfeed

# Fetch articles as JSON
fetch-json:
	cd packages/stonksfeed && uv run stonksfeed --format json

# Fetch RSS feeds only
fetch-rss:
	cd packages/stonksfeed && uv run stonksfeed --rss-only

# Fetch forum posts only
fetch-forums:
	cd packages/stonksfeed && uv run stonksfeed --forums-only

# Build stonksfeed package for Lambda
build-lambda:
	./scripts/build-lambda.sh

# Frontend dev server
frontend-dev:
	cd frontend && npm run dev

# Frontend production build
frontend-build:
	cd frontend && npm run build

# Full build (frontend + lambda package)
build: build-lambda frontend-build
	@echo "Build complete!"
