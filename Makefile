build:
	docker-compose -f docker-compose.dev.yml build --pull

up:
	docker-compose -f docker-compose.dev.yml up -d

down:
	docker-compose -f docker-compose.dev.yml down -v

start: build up

tests:
	PYTHONPATH=galangal/ python -m pytest galangal/tests --verbose --disable-warnings --cov=galangal/

isort:
	PYTHONPATH=galangal/ isort galangal/ -m=3

linter:
	PYTHONPATH=galangal/ pylint galangal/

cli:
	python galangal/manage_cli.py search
