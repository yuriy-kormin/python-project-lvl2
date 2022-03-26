install:
	poetry install

lint:
	poetry run flake8 gendiff

build:
	poetry build

test:
	poetry run pytest

coverage:
	poetry run pytest --cov=gendiff