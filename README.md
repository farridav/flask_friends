# Gamesys

## Getting Started

### Development
Make sure the following environment variables have been set:

    export APP_SECRET_KEY='my-secret-key'
    export APP_FACEBOOK_APP_ID='yourappid'
    export APP_FACEBOOK_APP_SECRET='your app secret'

A convenient way to do this is in your virtualenvs activate script,
or as a standalone `.env` file that you manually source

Setup a virtualenv, e.g:-

    virtualenv .venv && . .venv/bin/activate

Install the requirements and the test requirements

    pip install -r requirements.txt
    pip install -r test-requirements.txt

Run flake8, and the tests

    flake8 --exclude .venv
    nosetests

#!/bin/bash
