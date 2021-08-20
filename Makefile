ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.DEFAULT_GOAL := help


help:
	@grep -E '^[a-zA-Z0-9_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

run:  ## Run development environment
	cd src && ./env/bin/python main.py

setup:  ## install requirements
	./env/bin/pip install -r requirements.txt

isort:  ## sort imports
	cd src && isort .

black:  ## reformat code
	cd src && black .
