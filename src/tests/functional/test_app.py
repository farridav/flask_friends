from unittest import TestCase
import os

from google.appengine.ext import testbed
from google.appengine.ext.ndb import delete_multi
from mock import patch, Mock

from friends import app
from friends.auth import User

from tests.factories import friends_json


class AppTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Setup our testbed so we can interact with mock
        GAE services, and get a flask test client for
        making requests
        """
        super(AppTestCase, cls).setUpClass()
        cls.app = app.test_client()
        cls.testbed = testbed.Testbed()
        cls.testbed.activate()
        cls.testbed.init_datastore_v3_stub()
        cls.testbed.init_user_stub()
        cls.testbed.init_memcache_stub()

    @classmethod
    def tearDownClass(cls):
        """
        Cleanup our testbed
        """
        super(AppTestCase, cls).tearDownClass()
        cls.testbed.deactivate()

    def tearDown(self):
        """
        Logout our current user and make sure all users
        are deleted from the data store
        """
        super(AppTestCase, self).tearDown()
        self.logout()
        delete_multi([user.key for user in User.query()])

    def login(self, email, pw):
        """
        Make a user if we need to, and log them in
        """
        user = User.get_or_insert(
            email, email=email, password=pw)

        return self.app.post('/login', data=dict(
            email=user.email,
            pw=pw
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

    def test_bad_user_login(self):
        """
        A non-existent user tries to login, and doesnt
        opt in for registration... gets nowhere
        """
        email, password = 'new@email.com', 'password'
        response = self.app.post('/login', data={
            'email': email, 'pw': password
        })

        self.assertIn(
            'Wrong username and/or password',
            response.data
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            len(User.query(User.email == email).fetch()), 0
        )

    def test_user_registration(self):
        """
        When a user asks to be registered, they are
        """
        email, password = 'new@email.com', 'password'
        response = self.app.post('/login', data={
            'email': email, 'pw': password,
            'register': True
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            len(User.query(User.email == email).fetch()), 1
        )

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

    def test_api_friends_stores_in_db(self):
        """
        We only ever hit facebook for friends once, after
        that we fetch them out of the database
        (unless we require pagination, which our test data doesnt)
        """
        self.login('david@test.com', 'david')

        with patch('friends.facebook.facebook') as facebook:
            facebook.get.return_value = Mock(data=friends_json())
            # Call the friends list multiple times
            self.app.get('/api/friends')
            self.app.get('/api/friends')

        self.assertEqual(facebook.get.call_count, 1)

    def test_facebook_webhook_verification(self):
        """
        When we (poasing as facebook) hit our callback endpoint
        with GET, we have to confirm verify token and return
        """
        self.login('david@test.com', 'david')
        token = 'testing'
        os.environ['FB_CALLBACK_TOKEN'] = token

        response = self.app.get(
            '/api/friends/webhook?hub.verify_token={}'.format(
                token
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, token)

    def test_facebook_callback_auth(self):
        """
        Smoketest facebook auth calllback

        N.B - Does not test any part of the oAuth flow
        """
        self.login('david@test.com', 'david')

        response = self.app.get('/facebook/authorized')

        self.assertEqual(response.status_code, 200)

    def test_facebook_deauth(self):
        """
        Test we can deauthorize a user and clean up after
        them

        TODO:
            - Assert user marked as inactive
            - Assert token removed
            - Assert webhook unsubscribed?
        """
        self.login('david@test.com', 'david')

        response = self.app.get('/facebook/deauthorized')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'ok')
