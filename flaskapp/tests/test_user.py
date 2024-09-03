import unittest
from flaskapp import db
from flaskapp.models import User
from tests.base import BaseTestCase

class UserModelTestCase(BaseTestCase):
    def test_create_user(self):
        user = User(name='John Doe', email='john@example.com', auth_provider='google', provider_id='google123')
        db.session.add(user)
        db.session.commit()
        
        queried_user = User.query.filter_by(provider_id='google123').first()
        self.assertIsNotNone(queried_user)
        self.assertEqual(queried_user.name, 'John Doe')

    def test_get_users(self):
        user = User(name='John Doe', email='john@example.com', auth_provider='google', provider_id='google123')
        db.session.add(user)
        db.session.commit()

        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn('John Doe', str(response.data))

    def test_get_user(self):
        self.client.post('/users', json={
            'auth_provider': 'google',
            'provider_id': 'google123',
            'name': 'Test User',
            'email': 'testuser@example.com'
        })
        response = self.client.get('/users/google123', json={
            'auth_provider': 'google',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test User', str(response.data))

    def test_update_user(self):
        self.client.post('/users', json={
            'name': 'testuser',
            'email': 'testuser@example.com',
            'auth_provider': 'google',
            'provider_id': 'google123'
        })
        response = self.client.put('/users/google123', json={
            'name': 'testuser_updated',
            'email': 'testuser@example.com',
            'auth_provider': 'google',
            'provider_id': 'google123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('testuser_updated', str(response.data))

    def test_delete_user(self):
        self.client.post('/users', json={
            'name': 'testuser',
            'email': 'testuser@example.com',
            'auth_provider': 'google',
            'provider_id': 'google123'
        })
        response = self.client.delete('/users/google123', json={
            'auth_provider': 'google'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('User deleted', str(response.data))

if __name__ == '__main__':
    unittest.main()
