#!env/bin/python

from friends import app
from friends.views import (
    login, logout, home,
    facebook_authorized, api_friends
)

app.run()
