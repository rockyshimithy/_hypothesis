.PHONY: help
SHELL := /bin/bash
PROJECT_NAME = hypothesis

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

clean:  ## Clean python bytecodes, optimized files, logs, cache, coverage...
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -rf htmlcov/
	@rm -fr .pytest_cache/
	@rm -f coverage.xml
	@rm -f *.log
	@find . -name "celerybeat-schedule*" | xargs rm -rf

init-env:  ## create a .env file with the environment variables.
	@cp etc/env.sample .env
	@echo '.env file initialized at the project root. Customize it as you may.'

requirements:  ## Install pip requirements
	@pip install --upgrade pip
	@pip install -r requirements.txt

style:	## Run isort and black auto formatting code style in the project
	@echo 'running isort...'
	@isort -m 3 --trailing-comma --use-parentheses --honor-noqa .
	@echo 'running black...'
	@black -S -t py39 -l 79 $(PROJECT_NAME)/. --exclude '/(\.git|\.venv|env|build|dist)/'

style-check:  ## Run isort and black check code style
	@echo 'isort check...'
	@isort -v --check -m 3 --trailing-comma --use-parentheses --honor-noqa --color .
	@echo 'black check...'
	@black -S -t py37 -l 79 --check $(PROJECT_NAME)/. --exclude '/(\.git|\.venv|env|build|dist)/'

