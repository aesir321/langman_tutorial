# langman_tutorial

This tutorial is following the course available at educative.io called "Quick Start Full Stack Web Development". All instructions are assumed to be run in the root directory of the repository.

## Developer Setup

### Clone the repository

### Configure python environment

- `python -m pip install --user pipx`
- `pipx install poetry`
- `poetry install`

### Install git hook scripts

- `poetry run pre-commit install`

### Create database

- `wget https://github.com/socratecha/frapbook-v1.0-langman/raw/master/data/usages.csv`
- `mkdir data`
- `mv usages.csv data/`
- `export FLASK_APP=server.prepare_orm`
- `export FLASK_ENV=dev_lite`
- `export LC_ALL=C.UTF-8 && export LANG=C.UTF-8`
- `poetry run flask init-db`

### Install SQLite3 REPL

- Mac: `brew install sqlite`
- Windows: `choco install sqlite`
- Linux: `apt install sqlite`

### Set environment variables

- Update the `.env` and `.flaskenv` files changing the values of the environment variables where necessary.
