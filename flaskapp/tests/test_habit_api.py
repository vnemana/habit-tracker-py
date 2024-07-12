import unittest
import json
from flaskapp import db
from flaskapp.models import User, Habit
from tests.base import BaseTestCase

class HabitApiTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client = self.app.test_client()
        # Create a user for testing
        self.user = User(username='testuser', password='password')
        db.session.add(self.user)
        db.session.commit()

    def test_create_habit(self):
        response = self.client.post('/habits', data=json.dumps({
            'user_id': self.user.id,
            'name': 'Exercise',
            'frequency': 'Daily',
            'time_of_day': None
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.data)
        self.assertIn('id', data)

        queried_habit = Habit.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(queried_habit)
        self.assertEqual(queried_habit.name, 'Exercise')

    def test_get_habits(self):
        habit = Habit(user_id=self.user.id, name='Exercise', frequency='Daily', time_of_day=None)
        db.session.add(habit)
        db.session.commit()
        
        response = self.client.get('/habits')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Exercise', str(response.data))

    def test_get_habit(self):
        self.client.post('/habits', json={
            'user_id': 1,
            'name': 'Test Habit',
            'frequency': 'Daily',
            'time_of_day': '2024-07-10T08:00:00'
        })
        response = self.client.get('/habits/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Habit', str(response.data))

    def test_update_habit(self):
        self.client.post('/habits', json={
            'user_id': 1,
            'name': 'Test Habit',
            'frequency': 'Daily',
            'time_of_day': '2024-07-10T08:00:00'
        })
        response = self.client.put('/habits/1', json={
            'user_id': 1,
            'name': 'Updated Habit',
            'frequency': 'Weekly',
            'time_of_day': '2024-07-10T08:00:00'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Updated Habit', str(response.data))

    def test_delete_habit(self):
        self.client.post('/habits', json={
            'user_id': 1,
            'name': 'Test Habit',
            'frequency': 'Daily',
            'time_of_day': '2024-07-10T08:00:00'
        })
        response = self.client.delete('/habits/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Habit deleted', str(response.data))


if __name__ == '__main__':
    unittest.main()
