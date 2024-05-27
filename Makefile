.PHONY: format

BIN := ./.venv/bin

format:
	@${BIN}/ruff check --fix feature_flags
	@${BIN}/ruff format feature_flags