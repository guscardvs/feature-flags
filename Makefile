.PHONY: format test

BIN := ./.venv/bin

format:
	@${BIN}/ruff check --fix code_flags
	@${BIN}/ruff format code_flags

test:
	@${BIN}/pytest tests