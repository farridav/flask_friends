import os
from unittest import TestCase

from friends import app


class AppTestCase(TestCase):

    def setUp(self):
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
        Viewing the friends page, we get a redirect to
        the facebook auth dialog
        """
        response = self.app.get('/friends')

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.location.startswith(
            'https://www.facebook.com/dialog/oauth'
        ))

    def test_protected_view_locked_down(self):
        """
        Our protected view, is
        """
        response = self.app.get('/protected')

        self.assertEqual(response.status_code, 302)
        self.assertTrue('login' in response.location)

    def test_login_view(self):
        """
        Our Login view logs us in as expected
        """
        email = 'david@test.com'
        response = self.login(email, 'david')

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'Welcome {}'.format(email), response.data
        )

    def test_protected_view_accessible(self):
        """
        Our protected view can be accessed when logged in
        """
        self.login('david@test.com', 'david')

        response = self.app.get('/protected')

        self.assertEqual(response.status_code, 200)
