format: lint
	uv run -- ruff format

lint:
	uv run -- ruff check --fix

test:
	uv run -- pytest

setup:
	uv sync --frozen --compile-bytecode
	uv run -- pre-commit install --install-hooks

run:
	uv run -- python -m src.main