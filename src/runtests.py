#!/usr/bin/env python

import os
import sys
import unittest

THIS_DIR = os.path.dirname(__file__)
ENV_YML = os.path.join(THIS_DIR, 'env.yaml')
GIT_IGNORE = os.path.join(THIS_DIR, '../', '.gitignore')

# Add our library paths
sys.path.insert(1, os.path.join(THIS_DIR, 'lib'))
sys.path.insert(1, os.path.join(THIS_DIR, 'friends'))

import yaml  # NOQA
from flake8.engine import get_style_guide  # NOQA
from flake8.main import DEFAULT_CONFIG, print_report  # NOQA

with open(ENV_YML) as env_file:
    env = yaml.load(env_file.read())

for key, value in env.iteritems():
    os.environ.setdefault(key, value)

# Add the app engin SDK path
sys.path.insert(0, os.getenv('SDK_PATH'))

# Only now can we import our app as it uses appengine
# libs
import friends  # NOQA

import dev_appserver  # NOQA

dev_appserver.fix_sys_path()

if __name__ == '__main__':
    """
    Run flake8 checks. then nosetests
    """
    flake8_style = get_style_guide(
        exclude=','.join([
            l.strip() for l in
            open(GIT_IGNORE).readlines()
        ]), config_file=DEFAULT_CONFIG
    )
    report = flake8_style.check_files('./')
    if report.total_errors > 0:
        print_report(report, flake8_style)
        sys.exit(1)

    runner = unittest.TextTestRunner(verbosity=2)
    tests = unittest.loader.TestLoader().discover(
        os.path.join(THIS_DIR, 'tests')
    )
    failures = runner.run(tests)

    if failures > 0:
        sys.exit(1)
