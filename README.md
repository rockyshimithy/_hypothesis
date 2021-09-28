# \_hypothesis

This is a minimal financial project written in flask to provide an API to handle transactions between customers.

## Features

- Create customer
- List customers, filtering by name or identifier
- Create transaction, **given two different customers created before**
- List transactions, filtering by date and/or customer identifier

## Tech Stack

- Python 3.9.1
- Flask
- Marshmallow
- SqlAlchemy
- Postgres
- [Other Python packages](requirements/requirements.in)

**_NOTE:_**

- To provide code quality and standardization throughout the codebase, the tools below are installed and configured:
  - Black as code formatter
  - Isort to fix import order
  - Pylint as linter
- Tests were made with Pytest, with some plugins and freezegun because is fun travel through time
- Environment variables are used as configuration through [python-decouple](https://github.com/henriquebastos/python-decouple)
- Dockerfile to run the application on Docker using gunicorn

## Run Locally

Before start, it's necessary create and activate a virtualenv with `Python 3.9.1`, to do it I really recommend `pyenv`.

1.  Clone the project on your machine and go to the root folder of this project (_hypothesis)
```bash
git clone git@github.com:rockyshimithy/_hypothesis.git
cd _hypothesis
```

2. Run docker-compose to start Postgres
```bash
make docker-compose-up
```

3. Create an `.env` file with the specific configurations
```bash
make init-env
```
**_NOTE:_** If necessary and you are struggling with some docker network stuff, you can run the following command and discovery the IP address to set on `.env` file in `DB_HOST` variable.

```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <postgres_container_identifier>
```

4. With the env activated install project requirements
```bash
make requirements-pip
```

```bash
make init-db
```

```bash
make migrate
```

```bash
make upgrade
```

To move on, choose how to run the application given the options below.

### Option 1 - Run on Docker

5. Build the application image
```bash
make docker-build-image
```

6. Then, run it
```bash
make docker-run-server
```

### Option 2 - Run on a Python Environment

5. Run the application
```bash
make runserver-dev
```

## Running Tests

To run tests, run the following command
```bash
make test
```

To run coverage, run the following command
```bash
make coverage
```

**_NOTE:_** Consider be in an Python Environment with the packages installed

## Documentation

- TODO: Configure flasgger

## Deployment

You can deploy this project on production with your Docker orchestrator of choice.

## REPL

```bash
make shell
```

**_NOTE:_** Consider be in an Python Environment with the packages installed

## Enhancements that can be applied to this project

- Run `make style / make lint / make coverage` on github actions as continuous integration
- Create more tests to transactions and customers looking for bad scenarios
- Configure swagger using flasgger
- To able this application run on a production environment closier to reality, write a helm chart or yaml files need to deploy this project on k8s

## Feedback

Feel free to create an issue on this repository with feedbacks or suggestions.