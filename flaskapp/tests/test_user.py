import unittest
from flaskapp import db
from flaskapp.models import User
from tests.base import BaseTestCase

class UserModelTestCase(BaseTestCase):
    def test_create_user(self):
        user = User(username='testuser', password='password')
        db.session.add(user)
        db.session.commit()
        
        queried_user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(queried_user)
        self.assertEqual(queried_user.username, 'testuser')

    def test_get_users(self):
        user = User(username='testuser', password='password')
        db.session.add(user)
        db.session.commit()
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn('testuser', str(response.data))

    def test_get_user(self):
        self.client.post('/users', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('testuser', str(response.data))

    def test_update_user(self):
        self.client.post('/users', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        response = self.client.put('/users/1', json={
            'username': 'updateduser',
            'password': 'newpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('updateduser', str(response.data))

    def test_delete_user(self):
        self.client.post('/users', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        response = self.client.delete('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('User deleted', str(response.data))

if __name__ == '__main__':
    unittest.main()
