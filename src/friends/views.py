import json
import os
from time import sleep

from flask import (
    redirect, url_for, session, request,
    render_template, Response, abort, views
)

from .auth import flask_login, User
from .facebook import facebook, get_friends


class Login(views.View):
    """
    GET our login page, or with POST, Log our user
    in, optionally registering them first
    """

    def dispatch_request(self):
        if request.method == 'GET':
            return render_template('login.html')

        email = request.form.get('email')
        password = request.form.get('pw')
        register = request.form.get('register', False)

        user = User.query(
            User.email == email,
            User.password == password
        ).get()

        if not user and register:
            user = User(email=email, password=password)
            user.put()

        if user:
            flask_login.login_user(user)

            # TODO: fix race condition,
            # perhaps with signals
            sleep(2)

            return redirect(url_for('friends'))

        return Response(render_template('basic.html', **{
            'page_title': 'Access Denied',
            'content': 'Wrong username and/or password'
        }), status=401)


class Logout(views.View):
    """
    Log our user out, if we dont have a user, move on
    gracefully with 'Anonymous'
    """

    def dispatch_request(self):
        user_id = getattr(
            flask_login.current_user, 'id', 'Anonymous'
        )

        flask_login.logout_user()

        return Response(render_template('basic.html', **{
            'page_title': 'Logged Out',
            'content': 'Bye {}'.format(
                user_id
            )
        }), status=200)


class Home(views.View):
    """
    Load our home page

    N.B - Could be served as static
    """
    def dispatch_request(self):
        return Response(
            render_template('home.html'), status=200
        )


class FacebookAuthorized(views.View):
    """
    Receive the callback from facebook with our
    access_token
    """

    @facebook.authorized_handler
    def dispatch_request(response, self):
        """
        N.B - decorator is returning args backwards :(

        TODO: persist oauth_token into db?
        """
        if response is None:
            return '{} [{}]'.format(
                response.get('error_reason'),
                response.get('error_description')
            )

        session['oauth_token'] = (response['access_token'], '')

        return redirect(url_for('friends'))


class Friends(views.View):
    """
    Render out our friends page

    N.B Could be static, as friends are fetch from API
    """

    @flask_login.login_required
    def dispatch_request(self):
        if 'oauth_token' in session:
            return render_template('friends.html')

        return facebook.authorize(callback=url_for(
            'facebook_authorized',
            next=request.args.get('next') or request.referrer or None,
            _external=True
        ))


# API Routes

class APIFriends(views.View):
    """
    Protected API endpoint for retrieving our friends list
    """

    @flask_login.login_required
    def dispatch_request(self):
        """
        If we are logged in, store and return our friends
        """

        # If we dont yet have friends, get some :)
        if not flask_login.current_user.friends:
            flask_login.current_user.friends = get_friends()
            flask_login.current_user.put()

        friends = flask_login.current_user.friends

        return Response(
            json.dumps(friends),
            mimetype='application/json',
            headers={
                'Cache-Control': 'no-cache',
                'Access-Control-Allow-Origin': '*'
            }, status=200
        )


class APIFriendsWebHook(views.View):
    """
    The webhook facebook will receive POST from facebook when a
    users friends have been updated, take the updates, and store
    them against our users db stored friends
    """
    def dispatch_request(self):
        their_token = request.args.get('hub.verify_token', '')
        our_token = os.getenv('FB_CALLBACK_TOKEN')

        if their_token != our_token:
            abort(401)

        # GET's are used for endpoint verification,
        # return with our thing
        if request.method == 'GET':
            response = request.args.get('hub.something?', '')

        # Deal with the response (hub.something?)
        if request.method == 'POST':
            response = ''

        return Response(response, status=200)
