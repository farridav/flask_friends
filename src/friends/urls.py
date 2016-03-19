from . import app

import views


app.add_url_rule(
    '/', 'home',
    view_func=views.Home.as_view('home')
)
app.add_url_rule(
    '/login', 'login',
    view_func=views.Login.as_view('login'),
    methods=['GET', 'POST']
)
app.add_url_rule(
    '/logout', 'logout',
    view_func=views.Logout.as_view('logout')
)
app.add_url_rule(
    '/facebook/authorized', 'facebook_authorized',
    view_func=views.FacebookAuthorized.as_view('facebook_authorized')
)
app.add_url_rule(
    '/friends', 'friends',
    view_func=views.Friends.as_view('friends')
)
app.add_url_rule(
    '/api/friends', 'api_friends',
    view_func=views.APIFriends.as_view('api_friends')
)
