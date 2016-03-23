import json
from time import sleep

from flask import (
    redirect, url_for, session, request,
    render_template, Response
)
from flask.views import View

from .auth import flask_login, User
from .facebook import facebook, get_friends


class Login(View):

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


class Logout(View):

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


class Home(View):
    """
    Load our home page, Should be served as static really
    """
    def dispatch_request(self):
        return Response(
            render_template('home.html'), status=200
        )


class FacebookAuthorized(View):

    @facebook.authorized_handler
    def dispatch_request(response, self):
        """
        Receive the callback from facebook with our
        access_token

        N.B - decorator is returning args backwards :(
        """
        if response is None:
            return '{} [{}]'.format(
                response.get('error_reason'),
                response.get('error_description')
            )

        # TODO: persist this into the db?
        session['oauth_token'] = (response['access_token'], '')

        return redirect(url_for('friends'))


class Friends(View):

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

class APIFriends(View):
    """
    Endpoint for retrieving our friends list
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


class APIFriendsWebHook(View):
    def dispatch_request(self):
        return Response(
            'ok webhook called', status=200
        )
