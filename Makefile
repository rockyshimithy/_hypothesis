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
	@pip install -r requirements/base.txt

requirements-dev:  ## Install development pip requirements
	@pip install --upgrade pip
	@pip install -r requirements/development.txt

docker-compose-up: clean  ## Raise docker-compose for development environment
	@docker-compose up -d

docker-compose-stop: clean  ## Stop docker-compose for development environment
	@docker-compose stop

docker-compose-rm: docker-compose-stop ## Delete the development environment containers
	@docker-compose rm -f

runserver-dev: clean ## Run flask development server
	set -a && source .env && set +a && python dev-server.py

runserver: clean init-env ## Run gunicorn production server
	 # Gunicorn needs to bind to 0.0.0.0 so to be able to receive requests from the docker network,
	 # otherwise it will only receive them locally. With '-' logs are redirected to stdout (because containers)
	 # /dev/shm tells to the workers to use shared memory, and in-memory filesystem, instead of
	 # using files, which are slower and can degrade performance - and are not a good practice for
	 # containers anyhow, since they must redirect all of theirs logs to stdout/stderr.
	 set -a && source .env && set +a && gunicorn --worker-tmp-dir /dev/shm -c gunicorn_settings.py hypothesis:app -b 0.0.0.0:5000 --log-level INFO  --access-logfile '-' --error-logfile '-'

shell: clean ## initialize a shell
	 set -a && source .env && set +a && flask shell

routes:  ## show all configured api routes
	 set -a && source .env && set +a && flask routes

style:  ## Run isort and black auto formatting code style in the project
	@echo 'running isort...'
	@isort -m 3 --trailing-comma --use-parentheses --honor-noqa .
	@echo 'running black...'
	@black -S -t py39 -l 79 $(PROJECT_NAME)/. --exclude '/(\.git|\.venv|env|build|dist)/'

style-check:  ## Run isort and black check code style
	@echo 'isort check...'
	@isort -v --check -m 3 --trailing-comma --use-parentheses --honor-noqa --color .
	@echo 'black check...'
	@black -S -t py37 -l 79 --check $(PROJECT_NAME)/. --exclude '/(\.git|\.venv|env|build|dist)/'

lint:  ## Run the linter to enforce our coding practices
	@printf '\n --- \n >>> Running linter...<<<\n'
	@pylint --rcfile=.pylintrc $(PROJECT_NAME)/*
	@printf '\n FINISHED! \n --- \n'
