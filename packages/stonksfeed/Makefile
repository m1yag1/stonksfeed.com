.PHONY: install dev test lint format typecheck clean fetch build

# Install the package in development mode
install:
	uv sync

# Install with dev dependencies
dev:
	uv sync --all-extras

# Run tests
test:
	uv run pytest tests/ -v

# Run tests with coverage
coverage:
	uv run pytest tests/ -v --cov=stonksfeed --cov-report=term-missing

# Run linter
lint:
	uv run ruff check src/ tests/

# Format code
format:
	uv run ruff format src/ tests/
	uv run ruff check --fix src/ tests/

# Type checking
typecheck:
	uv run mypy src/stonksfeed

# Clean up
clean:
	rm -rf __pycache__ .pytest_cache .ruff_cache .mypy_cache
	rm -rf src/*.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Fetch articles (for local testing)
fetch:
	uv run stonksfeed

# Fetch RSS only
fetch-rss:
	uv run stonksfeed --rss-only

# Fetch forums only
fetch-forums:
	uv run stonksfeed --forums-only

# Output as JSON
fetch-json:
	uv run stonksfeed --format json

# Build wheel for Lambda
build:
	uv build --wheel
