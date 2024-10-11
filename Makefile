format:
	@ruff check . --fix && ruff format .

test:
	@pytest --cov .
