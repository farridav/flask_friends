import os
import json

from flask import (
    Flask, redirect, url_for, session, request,
    render_template, Response, abort
)

from . import app
from .auth import flask_login, users, User
from .facebook import facebook, get_friends


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    if email in users and request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return abort(403)


@app.route('/logout')
def logout():
    user_id = getattr(
        flask_login.current_user, 'id',
        'Anonymous'
    )
    flask_login.logout_user()

    return render_template('basic.html', **{
        'page_title': 'Logged Out',
        'content': 'Bye {}'.format(
            user_id
        )
    })


@app.route('/protected')
@flask_login.login_required
def protected():
    return render_template('basic.html', **{
        'page_title': 'Logged In',
        'content': 'Welcome {}'.format(
            flask_login.current_user.id
        )
    })


@app.route('/')
def home():
    """
    Load our home page, Should be served as static really
    """
    return render_template('home.html')


@app.route('/facebook/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return '{} [{}]'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    # TODO: persist this into the db?
    session['oauth_token'] = (resp['access_token'], '')

    return redirect(url_for('friends'))


@app.route('/friends')
def friends():
    if 'oauth_token' in session:
        return render_template('friends.html')

    return facebook.authorize(callback=url_for(
        'facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    ))


# API Routes
@app.route('/api/friends')
def api_friends():
    """
    Endpoint for retrieving our friends list
    """
    friends = get_friends()
    return Response(
        json.dumps(friends),
        mimetype='application/json',
        headers={
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        }
    )
