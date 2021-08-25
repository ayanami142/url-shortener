ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.DEFAULT_GOAL := help


help:
	@grep -E '^[a-zA-Z0-9_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

run-dev:  ## Run development environment
	./env/bin/python run.py

run-prod:  ## Run production environment
	gunicorn -w 4 run:app

setup:  ## install requirements
	python3 -m virtualenv env && source ./env/bin/activate && ./env/bin/python -m pip install -U pip && ./env/bin/pip install -r requirements.txt

isort:  ## sort imports
	cd src && isort .

black:  ## reformat code
	cd src && black .

migrate: ## apply migrations
	cd src && flask db upgrade

tests: ## run unit tests
	./env/bin/python -m unittest discover -s src/tests -t src/tests
