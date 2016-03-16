import os
import json

from flask_oauth import OAuth

from .app import app, THIS_DIR

oauth = OAuth()

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


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')
