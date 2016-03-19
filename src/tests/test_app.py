from unittest import TestCase

from google.appengine.ext import testbed

from friends import app
from friends.auth import User


class AppTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.testbed = testbed.Testbed()
        cls.testbed.activate()
        cls.testbed.init_datastore_v3_stub()
        cls.testbed.init_user_stub()
        cls.testbed.init_memcache_stub()

    @classmethod
    def tearDownClass(cls):
        cls.testbed.deactivate()

    def tearDown(self):
        self.logout()

    def login(self, email, pw):
        """
        Make a user if we need to, and log them in
        """
        user = User.get_or_insert(
            email, email=email, password=pw)

        return self.app.post('/login', data=dict(
            email=user.email,
            pw=user.password
        ))

    def logout(self):
        """
        Log our user out (via the view)
        """
        return self.app.get('/logout', follow_redirects=True)

    def test_redirect_to_social_login(self):
        """
        Viewing the friends page as a logged in user,
        we get a redirect to the facebook auth
        """

        self.login('david@test.com', 'david')

        response = self.app.get('/friends')

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.location.startswith(
            'https://www.facebook.com/dialog/oauth'
        ))

    def test_friends_view_locked_down(self):
        """
        Our friends view redirects us to login,
        if we are not already logged in
        """
        response = self.app.get('/friends')

        self.assertEqual(response.status_code, 302)
        self.assertTrue('login' in response.location)

    def test_login_view(self):
        """
        Our Login view logs us in as expected
        """
        email = 'david@test.com'
        response = self.login(email, 'david')

        self.assertEqual(response.status_code, 302)
        self.assertTrue('friends' in response.location)

    def test_friends_view_accessible(self):
        """
        Our friends view can be accessed when logged in
        """
        self.login('david@test.com', 'david')

        response = self.app.get('/friends')

        self.assertEqual(response.status_code, 302)
        self.assertTrue('friends' in response.location)
