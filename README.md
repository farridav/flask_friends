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
    APP_FB_APP_ID: 'yourappid'
    APP_FB_APP_SECRET: 'your app secret'
    SDK_PATH: '/path/to/google_appengine/'

N.B - This file is kept out of version control

Install the requirements (GAE)

    pip install -r dev-requirements.txt -t src/lib

### Static files/libs
I am using bower to manage frontend deps, but dont want too much extra cruft in there,
so for now, im rsyncing in, as follows:

    npm install bower
    ./node_modules/bower/bin/bower i
    rsync -avz ./bower_components/bootstrap/dist/ ./src/friends/static/lib/
    rsync -avz ./bower_components/jquery/dist/ ./src/friends/static/lib/js/
    rsync -avz ./bower_components/react/ ./src/friends/static/lib/js/
    rsync -avz ./bower_components/babel/ ./src/friends/static/lib/js/

https://github.com/twbs/bootstrap/releases/download/v3.3.6/bootstrap-3.3.6-dist.zip

### Running
To run this project with all of the mock appengine resources from the appengine SDK, use:

    dev_appserver.py src/

### Testing

Run flake8, and the tests with:

    ./src/runtests.py

### Deploying
This project has not yet been deployed, and has been developed solely using the SDK, a deployment guide can be found [here](https://github.com/GoogleCloudPlatform/appengine-flask-skeleton#deploy)
