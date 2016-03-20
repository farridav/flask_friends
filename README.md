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

### Development
Make sure the following environment variables have been set in src/env.yaml:

    APP_SECRET_KEY: 'my-secret-key'
    FB_APP_ID: 'yourappid'
    FB_APP_SECRET: 'your app secret'
    SDK_PATH: '/path/to/google_appengine/'

N.B - This file is kept out of version control

### Static files/libs

    ./update

### Running
To run this project with all of the mock appengine resources from the appengine SDK, use:

    dev_appserver.py src/

### Testing

Run flake8, and the tests with:

    ./src/runtests.py

### Deploying
This project has not yet been deployed, and has been developed solely using the SDK, a deployment guide can be found [here](https://github.com/GoogleCloudPlatform/appengine-flask-skeleton#deploy)
