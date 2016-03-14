# Gamesys

## Getting Started

### Development
Setup a virtualenv

    virtualenv .venv && . .venv/bin/activate

Install the requirements and the test requirements

    pip install -r requirements.txt
    pip install -r test-requirements.txt

Run flake8, and the tests

    flake8 --exclude .venv
    nosetests
