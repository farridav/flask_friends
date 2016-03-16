import os

from flask import Flask

THIS_DIR = os.path.dirname(__file__)
DEBUG = True

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = os.getenv('APP_SECRET_KEY')
