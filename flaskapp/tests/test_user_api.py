import unittest
import json
from flaskapp.models import User
from tests.base import BaseTestCase

class UserApiTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/users', data=json.dumps({
            'name': 'testuser',
            'email': 'testuser@example.com',
            'auth_provider': 'google',
            'provider_id': 'google-12345',
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.data)
        self.assertIn('id', data)

        queried_user = User.query.filter_by(name='testuser').first()
        self.assertIsNotNone(queried_user)
        self.assertEqual(queried_user.name, 'testuser')
        self.assertEqual(queried_user.auth_provider, 'google')

if __name__ == '__main__':
    unittest.main()
