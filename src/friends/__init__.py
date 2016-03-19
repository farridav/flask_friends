import os

from flask import Flask
from flask.ext import login

DEBUG = True
THIS_DIR = os.path.dirname(__file__)

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = os.getenv('APP_SECRET_KEY')

login_manager = login.LoginManager()
login_manager.init_app(app)

import urls
