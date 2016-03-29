import os

from flask import session
from flask_oauth import OAuth

oauth = OAuth()

FB_APP_ID = os.getenv('FB_APP_ID')
FB_APP_SECRET = os.getenv('FB_APP_SECRET')
FB_MAX_PAGER = 10

facebook = oauth.remote_app(
    'facebook',
    base_url='https://graph.facebook.com/v2.5/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FB_APP_ID,
    consumer_secret=FB_APP_SECRET,
    request_token_params={'scope': 'user_friends'}
)


def get_friends():
    """
    Get Our friends list, and keep following next hyperlinks until we have
    exhausted the API (or we hit our pager limit)
    """
    pager = 0
    url = '/me/taggable_friends?fields=name,picture{url}'
    data = facebook.get(url).data
    friends = data['data']

    while ('next' in data['paging']) and pager < FB_MAX_PAGER:
        next = '{}&after={}'.format(
            url, data['paging']['cursors']['after']
        )
        data = facebook.get(next).data
        friends.extend(data['data'])
        pager += 1

    return {
        'friends': friends
    }


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')
