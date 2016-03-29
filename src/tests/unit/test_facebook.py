from unittest import TestCase

from mock import patch, Mock

from friends.facebook import get_friends

from tests.factories import friends_json, friend


class FaceBookTestCase(TestCase):

    def test_friends_pagination(self):
        """
        When we recieve a friends list that requires pagination, we
        consume it all before storign and returning via the API
        """

        with patch('friends.facebook.facebook') as facebook:
            data = friends_json()

            # Add an additonal 'data' property, as this is present in
            # paginated facebook responses, and add a new friend
            data['data'] = [
                friend({"name": "Lenny Henry"}),
                friend({"name": "Fred Perry"})
            ]

            facebook.get.return_value = Mock(data=data)

            # Double our friends
            friends_count = data['friends']['summary']['total_count']
            new_friends_count = int(friends_count) + len(data['data'])
            data['friends']['summary']['total_count'] = new_friends_count

            # Call the friends list multiple times
            friends = get_friends()
            names = [f['name'] for f in friends['friends']]

        # Assert we have all of our friends
        self.assertEqual(len(friends['friends']), new_friends_count)

        # Assert our two new friends made it into the response
        self.assertTrue('Lenny Henry' in names)
        self.assertTrue('Fred Perry' in names)
