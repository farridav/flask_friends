"""
This File is read by google app engine, before starting the app,
it will also be run before dev_appserver.py
"""

import os
import yaml
from google.appengine.ext import vendor

THIS_DIR = os.path.dirname(__file__)
ENV_YML = os.path.join(THIS_DIR, 'env.yaml')

# Third-party libraries are stored in "lib", vendoring will make
# sure that they are importable by the application.
vendor.add(os.path.join(THIS_DIR, 'lib'))

# Load in env vars if found
if os.path.isfile(ENV_YML):
    with open(ENV_YML) as env_settings_file:
        env_settings = yaml.load(env_settings_file.read())

    # Using setdefault rather than update, as to avoid overriding
    for key, value in env_settings.iteritems():
        os.environ.setdefault(key, value)
