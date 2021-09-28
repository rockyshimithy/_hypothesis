.PHONY: help
SHELL := /bin/bash
PROJECT_NAME = hypothesis
CONTAINER_USER_ID = $$(id -u)
CONTAINER_GROUP_ID = $$(id -g)

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

export-flask-var:  ## Set FLASK_APP as env var
	@export FLASK_APP=$(PROJECT_NAME)/__init__.py

requirements-pip:  ## Install pip requirements
	@pip install --upgrade pip
	@pip install -r requirements/development.txt

init-db:  ## Start alembic with new DB
	@set -a && source .env && set +a && flask db init

migrate:  ## Create migrations
	@set -a && source .env && set +a && flask db migrate

upgrade-migrations:  ## Execute the migrations
	@set -a && source .env && set +a && flask db upgrade

docker-compose-up: clean  ## Raise docker-compose for development environment
	@docker-compose up -d

docker-compose-stop: clean  ## Stop docker-compose for development environment
	@docker-compose stop

docker-compose-rm: docker-compose-stop ## Delete the development environment containers
	@docker-compose rm -f

docker-build-image: clean  ## Build local docker image
	@docker build -t "$(PROJECT_NAME)" --pull --no-cache --build-arg CONTAINER_USER_ID="$(CONTAINER_USER_ID)" --build-arg CONTAINER_GROUP_ID="$(CONTAINER_GROUP_ID)" -f Dockerfile .

docker-run-server: clean  ## Run the app docker image locally
	@docker run --rm -d -p 5000:5000 --name hypothesis --env-file .env --network bridge hypothesis:latest

runserver-dev: clean  ## Run flask development server
	@set -a && source .env && set +a && python dev-server.py

runserver: clean  ## Run gunicorn production server
	# Gunicorn needs to bind to 0.0.0.0 so to be able to receive requests from the docker network,
	# otherwise it will only receive them locally. With '-' logs are redirected to stdout (because containers)
	# /dev/shm tells to the workers to use shared memory, and in-memory filesystem, instead of
	# using files, which are slower and can degrade performance - and are not a good practice for
	# containers anyhow, since they must redirect all of theirs logs to stdout/stderr.
	@set -a && source .env && set +a && gunicorn --worker-tmp-dir /dev/shm -c gunicorn_settings.py hypothesis:app -b 0.0.0.0:5000 --log-level INFO  --access-logfile '-' --error-logfile '-'

api-docs:  ## Show api docs (must be run on a desktop linux machine, with the app running locally)
	@xdg-open http://localhost:5000/apidocs

shell: clean  ## initialize a shell
	@set -a && source .env && set +a && flask shell

routes:  ## show all configured api routes
	@set -a && source .env && set +a && flask routes

style:  ## Run isort and black auto formatting code style in the project
	@echo 'running isort...'
	@isort -m 3 --trailing-comma --use-parentheses --honor-noqa .
	@echo 'running black...'
	@black -S -t py39 -l 79 $(PROJECT_NAME)/. --exclude '/(\.git|\.venv|env|build|dist)/'

lint:  ## Run the linter to enforce our coding practices
	@printf '\n --- \n >>> Running linter...<<<\n'
	@pylint --rcfile=.pylintrc $(PROJECT_NAME)/*
	@printf '\n FINISHED! \n --- \n'

test: clean  ## Run the test suite
	@cd $(PROJECT_NAME) && py.test -s -vvv

test-matching: clean  ## Run only tests matching pattern. E.g.: make test-matching test=TestClassName
	@cd $(PROJECT_NAME) && py.test -s -vvv -k $(test)

coverage: clean  ## Run the test coverage report
	@py.test --cov-config .coveragerc --cov $(PROJECT_NAME) $(PROJECT_NAME) --cov-report term-missing
