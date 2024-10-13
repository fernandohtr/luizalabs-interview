DOCKER_LOCAL:=docker compose -f local.yml

format:
	@ruff check . --fix && ruff format .

local:
	poetry export -f requirements.txt --with dev --without-hashes --without-urls -o requirements/local.txt

build:
	${DOCKER_LOCAL} up -d --build --remove-orphans

up:
	${DOCKER_LOCAL} up -d

stop:
	${DOCKER_LOCAL} stop

down:
	${DOCKER_LOCAL} down

logs:
	@${DOCKER_LOCAL} logs -f

test:
	${DOCKER_LOCAL} run --rm api pytest -p no:warnings --cov=/app/
