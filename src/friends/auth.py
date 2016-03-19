from google.appengine.ext import ndb

from flask import abort, url_for, redirect
import flask.ext.login as flask_login

from . import login_manager


class User(flask_login.UserMixin, ndb.Model):
    email = ndb.StringProperty(required=True, indexed=True, repeated=False)
    password = ndb.StringProperty(required=True, indexed=True)
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


@login_manager.request_loader
def request_loader(request):
    user = User.query(
        User.email == request.args.get('email')
    ).get()

    if not user:
        return

    user.is_authenticated = False

    return user


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))
