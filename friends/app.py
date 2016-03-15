import os
import json

from flask import (
    Flask, redirect, url_for, session, request,
    render_template, Response, abort
)
import flask.ext.login as flask_login
from flask_oauth import OAuth

DEBUG = True
THIS_DIR = os.path.dirname(__file__)

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = os.getenv('APP_SECRET_KEY')
oauth = OAuth()

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'david@test.com': {'pw': 'david'}}

FACEBOOK_APP_ID = os.getenv('APP_FACEBOOK_APP_ID')
FACEBOOK_APP_SECRET = os.getenv('APP_FACEBOOK_APP_SECRET')
FACEBOOK_MAX_PAGER = 10

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


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
        <form action='login' method='POST'>
        <input type='text' name='email' id='email' placeholder='email'></input>
        <input type='password' name='pw' id='pw' placeholder='password'></input>
        <input type='submit' name='submit'></input>
        </form>
        '''

    email = request.form['email']
    if email in users and request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return abort(401)


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


def get_friends():
    """
    Get Our friends list, and keep following next hyperlinks until we have
    exhausted the API (or we hit our pager limit)
    """

    cache = os.path.join(THIS_DIR, 'cache.json')

    if os.path.isfile(cache):
        data = json.load(open(cache))
        return {
            'name': data['name'],
            'friends': data['taggable_friends']['data'],
        }

    # Populate cache
    pager = 0
    data = facebook.get(
        '/me/?fields=name,friends,taggable_friends{name,picture{url}}&limit=100'
    ).data

    friends = data['taggable_friends']['data']

    while (len(friends) < int(data['friends']['summary']['total_count'])
           and pager < FACEBOOK_MAX_PAGER):
        friends.extend(facebook.get(
            data['taggable_friends']['paging']['next']
        ).data['data'])

        pager += 1

    with open(cache, 'wb+') as f:
        f.write(json.dumps(data))

    return {
        'name': data['name'],
        'friends': data['taggable_friends']['data'],
    }


@app.route('/')
def index():
    """
    Make sure we are authed with facebook, then render our app
    """
    if 'oauth_token' not in session:
        return redirect(url_for('social_login'))

    return render_template('index.html')


@app.route('/social-login')
def social_login():
    return facebook.authorize(callback=url_for(
        'facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True
    ))


@app.route('/social-login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return '{} [{}]'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    # TODO: persist this into the db?
    session['oauth_token'] = (resp['access_token'], '')

    return redirect(url_for('index'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


# API Routes
@app.route('/api/friends')
def friends():
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


if __name__ == '__main__':
    app.run()
