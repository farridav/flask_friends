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

Make sure you have the right [system packages](http://googlecloudplatform.github.io/gcloud-python/stable/) for gcloud

Install the requirements and the test requirements

    pip install -r requirements.txt
    pip install -r test-requirements.txt

### Running
To run this project with all of the mock appengine resources from the appengine SDK, use:

    dev_appserver.py src/

To run it directly use:

    python src/run.py

### Google Cloud platform
This project has been built to work with Googles cloud platform,
to interact with this in development, follow the guide [here](https://cloud.google.com/datastore/docs/tools/)
ensuring you Install the following SDK's:

    https://cloud.google.com/sdk/#deb
    https://cloud.google.com/appengine/downloads

Now setup gcloud with:

    gcloud init

install requirements here

    pip install -r requirements.txt -t src/lib/


### Testing

Run flake8, and the tests with:

    ./src/runtests.py
