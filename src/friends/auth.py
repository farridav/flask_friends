import hashlib

from google.appengine.ext import ndb

from flask import url_for, redirect
import flask.ext.login as flask_login

from . import login_manager, app


def hash_password(prop, value):
    """
    Hash our password with our salt
    """
    salt = app.secret_key
    return hashlib.sha512(value + salt).hexdigest()


class User(flask_login.UserMixin, ndb.Model):
    email = ndb.StringProperty(required=True, indexed=True, repeated=False)
    password = ndb.StringProperty(
        required=True, indexed=True,
        validator=hash_password
    )
    token = ndb.StringProperty(indexed=False)
    friends = ndb.JsonProperty(indexed=False)

    @property
    def id(self):
        return self.email


@login_manager.user_loader
def user_loader(email):
    """
    Given the users email, find and
    return the user
    """
    user = User.query(User.email == email).get()

    if not user:
        return

    return user


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))
