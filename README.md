# Gamesys

## Getting Started

### Development
Make sure the following environment variables have been set in src/env.yaml:

    APP_SECRET_KEY: 'my-secret-key'
    APP_FB_APP_ID: 'yourappid'
    APP_FB_APP_SECRET: 'your app secret'

N.B - This file is kept out of version control

Setup a virtualenv, e.g:-

    virtualenv .venv && . .venv/bin/activate

Install the requirements

    pip install -r dev-requirements.txt -t src/lib

### Google Cloud platform
This project has been built to work with Googles cloud platform, to interact with
this in development, follow the guide [here](https://cloud.google.com/datastore/docs/tools/)
ensuring you Install the following SDK's:

    https://cloud.google.com/sdk/#deb
    https://cloud.google.com/appengine/downloads

Now setup gcloud with:

    gcloud init

## Running
To run this project with all of the mock appengine resources from the appengine SDK, use:

    dev_appserver.py src/

### Testing

Run flake8, and the tests with:

    ./src/runtests.py
