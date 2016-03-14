import os

from flask import (
    Flask, redirect, url_for, session, request,
    render_template
)
from flask_oauth import OAuth


DEBUG = True
FACEBOOK_APP_ID = os.getenv('APP_FACEBOOK_APP_ID')
FACEBOOK_APP_SECRET = os.getenv('APP_FACEBOOK_APP_SECRET')

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = os.getenv('APP_SECRET_KEY')
oauth = OAuth()

facebook = oauth.remote_app(
    'facebook',
    base_url='https://graph.facebook.com/v2.5/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'user_friends'}
)


@app.route('/')
def index():
    if 'oauth_token' not in session:
        return redirect(url_for('login'))

    me = facebook.get('/me/?fields=name,taggable_friends{name,picture{url}}')

    return render_template('index.html', **{
        'name': me.data['name'],
        'friends': me.data['taggable_friends']['data']
    })


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for(
        'facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    ))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return '{} [{}]'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['oauth_token'] = (resp['access_token'], '')

    return redirect(url_for('index'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    app.run()
