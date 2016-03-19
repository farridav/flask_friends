# Gamesys

## Getting Started

### Development
Make sure the following environment variables have been set:

    export APP_SECRET_KEY='my-secret-key'
    export APP_FB_APP_ID='yourappid'
    export APP_FB_APP_SECRET='your app secret'

A convenient way to do this is in your virtualenvs activate script,
or as a standalone `.env` file that you manually source

Setup a virtualenv, e.g:-

    virtualenv .venv && . .venv/bin/activate

Make sure you have the right [system packages](http://googlecloudplatform.github.io/gcloud-python/stable/) for gcloud

Install the requirements and the test requirements

    pip install -r requirements.txt
    pip install -r test-requirements.txt

### Google Cloud platform
This project has been built to work with Googles cloud platform,
to interact with this in development, follow the guide [here](https://cloud.google.com/datastore/docs/tools/)
ensuring you Install the following SDK's:

    https://cloud.google.com/sdk/#deb
    https://cloud.google.com/appengine/downloads

Now setup gcloud with:

    gcloud init

### Testing

Run flake8, and the tests with:

    flake8 --exclude .venv
    ./tests.py
