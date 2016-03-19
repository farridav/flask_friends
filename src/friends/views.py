import json

from flask import (
    redirect, url_for, session, request,
    render_template, Response, abort
)
from flask.views import View

from .auth import flask_login, User, users
from .facebook import facebook, get_friends


class Login(View):

    def dispatch_request(self):
        if request.method == 'GET':
            return render_template('login.html')

        user = None
        email = request.form.get('email')
        password = request.form.get('pw')

        if email in users and users.get(email)['pw'] == password:
            user = User()
            user.id = email

        if user:
            flask_login.login_user(user)
            return redirect(url_for('protected'))

        return abort(403)


class Logout(View):

    def dispatch_request(self):
        user_id = getattr(
            flask_login.current_user, 'id', 'Anonymous'
        )

        flask_login.logout_user()

        return render_template('basic.html', **{
            'page_title': 'Logged Out',
            'content': 'Bye {}'.format(
                user_id
            )
        })


class Protected(View):

    @flask_login.login_required
    def dispatch_request(self):
        return render_template('basic.html', **{
            'page_title': 'Logged In',
            'content': 'Welcome {}'.format(
                flask_login.current_user.id
            )
        })


class Home(View):
    """
    Load our home page, Should be served as static really
    """
    def dispatch_request(self):
        return render_template('home.html')


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
    def dispatch_request(self):
        friends = get_friends()
        return Response(
            json.dumps(friends),
            mimetype='application/json',
            headers={
                'Cache-Control': 'no-cache',
                'Access-Control-Allow-Origin': '*'
            }
        )
