# Flask Friends
A test project made of the following components:

- Flask
- Bootstrap3
- ReactJS

Designed to be deployed to Googles app engine, the project is far from complete, but lives
to serve its purpose as a demonstration of skills.

## Getting Started

### Google App Engine (GAE)
This project has been built to work with Google App Engine, to interact with
this in development ensure you Install the following SDK's:

    https://cloud.google.com/sdk/#deb
    https://cloud.google.com/appengine/downloads

And setup gcloud with:

    gcloud init

### Configuration
Make sure the following environment variables have been set in src/env.yaml:

    APP_SECRET_KEY: 'my-secret-key'
    FB_APP_ID: 'yourappid'
    FB_APP_SECRET: 'your app secret'
    SDK_PATH: '/path/to/google_appengine/'

N.B - These values will change for production and development, and are kept out of version control

### Static files/libs

    ./update

### Running
To run this project with all of the mock appengine resources from the appengine SDK, use:

    dev_appserver.py src/

### Testing

Run flake8, and the tests with:

    ./src/runtests.py

### Deploying
For the first time:

    appcfg.py update -A flask-friends -V v1 src/

Subsequent times:

    appcfg.py set_default_version -V v<new_version no> -A flask-friends
