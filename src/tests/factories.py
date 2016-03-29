import os
import json


THIS_DIR = os.path.dirname(__file__)


def friends_json():
    """
    Return a mock json response from facebook
    """
    return json.load(
        open(os.path.join(THIS_DIR, 'friends.json'))
    )


def friend(updates={}):
    """
    Generate a json friend object, as returned in the facebook
    response, optionally, add your own customisations
    """
    friend = {
        "picture": {
            "data": {
                "url": "friend.jpg"
            }
        },
        "name": "Friend Name",
        "id": "friend_id"
    }

    friend.update(updates)

    return friend
