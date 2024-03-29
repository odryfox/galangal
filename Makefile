build:
	docker-compose -f docker-compose.dev.yml build --pull

up:
	docker-compose -f docker-compose.dev.yml up -d

down:
	docker-compose -f docker-compose.dev.yml down -v

start: build up

tests_build:
	docker-compose -f docker-compose.tests.yml build --pull

tests_up:
	docker-compose -f docker-compose.tests.yml up --abort-on-container-exit

tests: tests_build tests_up

isort:
	PYTHONPATH=galangal/ isort galangal/ -m=3

linter:
	PYTHONPATH=galangal/ pylint galangal/

cli:
	PYTHONPATH=apps/ python manage_cli.py
