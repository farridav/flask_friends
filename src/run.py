#!/usr/bin/env python

import os
import sys
import yaml

THIS_DIR = os.path.dirname(__file__)
ENV_YML = os.path.join(THIS_DIR, 'env.yaml')

with open(ENV_YML) as env_file:
    env = yaml.load(env_file.read())

for key, value in env.iteritems():
    os.environ.setdefault(key, value)

sys.path.insert(0, os.getenv('SDK_PATH'))
sys.path.insert(1, os.path.join(THIS_DIR, 'lib'))
sys.path.insert(1, os.path.join(THIS_DIR, 'friends'))

import dev_appserver
import friends

dev_appserver.fix_sys_path()

if __name__ == '__main__':
    friends.app.run(debug=True)
