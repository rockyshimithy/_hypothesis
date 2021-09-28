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

1.  Clone the project on your machine and go to the root folder of this project (_hypothesis)
```bash
  git clone git@github.com:rockyshimithy/_hypothesis.git
  cd _hypothesis
```

2. Execute docker-compose to start Postgres

```bash
  make docker-compose-up
```

To move on, choose how to run the application given the options below

# Option 1 - Run on Docker

```bash
  make docker-build-image
```

# Option 2 - Run on a Python Environment

Before start, it's necessary create and activate a virtualenv with `Python 3.9.1`, to do it I really recommend `pyenv`.

3. With the env activated Install project requirements

```bash
  make requirements-pip
```

[test](#features) 