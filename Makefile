# Common tasks. Every target is a thin wrapper; the real commands are visible below.
.DEFAULT_GOAL := help

.PHONY: help setup showdown server lint format test smoke clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

setup: ## Create the Python environment (uv) and install pre-commit hooks
	uv sync
	uv run pre-commit install

showdown: ## Clone and build Pokémon Showdown at the pinned commit (needs Node >= 22.18)
	scripts/setup_showdown.sh

server: ## Start a local Showdown server on port 8000 (Ctrl-C to stop)
	scripts/start_showdown.sh

lint: ## Lint and check formatting
	uv run ruff check .
	uv run ruff format --check .

format: ## Auto-fix lint issues and format
	uv run ruff check --fix .
	uv run ruff format .

test: ## Run unit tests (tests that need a server are skipped if none is running)
	uv run pytest

smoke: ## Battle the built-in bots on a running local server to prove the stack works
	uv run python scripts/smoke_battle.py --battles 10

clean: ## Remove caches and build output
	rm -rf .pytest_cache .ruff_cache build dist *.egg-info
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
