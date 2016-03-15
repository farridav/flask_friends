import os
from friends.app import app
import unittest
import tempfile


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def login(self, email, pw):
        return self.app.post('/login', data=dict(
            email=email,
            pw=pw
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_redirect_to_social_login(self):
        """
        Viewing the homepage gives us a 302 Found, and
        redirects us to /social-login
        """
        response = self.app.get('/')

        self.assertEqual(response.status_code, 302)
        self.assertTrue('social-login' in response.location)

    def test_protected_view_locked_down(self):
        """
        Our protected view, is
        """
        response = self.app.get('/protected')

        self.assertEqual(response.status_code, 401)

    def test_login_view(self):
        """
        Our Login view logs us in as expected
        """
        email = 'david@test.com'
        response = self.login(email, 'david')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            'Logged in as: {}'.format(email), response.data
        )

    def test_protected_view_accessible(self):
        """
        Our protected view can be accessed when logged in
        """
        self.login('david@test.com', 'david')

        response = self.app.get('/protected')

        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
