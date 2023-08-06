# Thabala CLI

Thabala Command Line Interface to interact with a Thabala account.

## Requirements

The thabala-cli package works on Python versions:

-  3.7.x and greater
-  3.8.x and greater
-  3.9.x and greater
-  3.10.x and greater

## Installation

The safest way to install Thabala CLI is to use [pip](https://pip.pypa.io/en/stable/) in a `virtualenv`:
```
$ python -m pip install thabala-cli
```

If you have the thabala-cli package installed and want to upgrade to the latest version, you can:
```
$ python -m pip install --upgrade thabala-cli
```

This will install the thabala-cli package as well as all dependencies.

## Development

On Linux and Mac:
```
python -m venv venv
. ./venv/bin/activate
python -m pip install --upgrade pip setuptools
pip install -r requirements.txt -r requirements-dev.txt
pip install -e .
```

On Windows:
```
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip setuptools
pip install -r requirements.txt -r requirements-dev.txt
pip install -e .
```

### pre-commit

Install `pre-commit` in the repo:
```
pre-commit install
```

### Testing

Python tests can be run with:

```
pytest
```
