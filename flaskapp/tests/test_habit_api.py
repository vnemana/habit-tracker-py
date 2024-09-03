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
        self.user = User(name='John Doe', email='john@example.com', auth_provider='google', provider_id='google123')
        db.session.add(self.user)
        db.session.commit()

    def test_create_habit(self):
        """Test Create habit from api."""
        response = self.client.post('/habits', data=json.dumps({
            'user_id': self.user.id,
            'name': 'Exercise',
            'frequency': 'Daily',
            'start_date': '2024-08-29',
            'time_of_day': '08:00:00'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.data)
        self.assertIn('id', data)

        queried_habit = Habit.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(queried_habit)
        self.assertEqual(queried_habit.name, 'Exercise')

    def test_get_habits(self):
        habit = Habit(user_id=self.user.id, name='Exercise', frequency='Daily', time_of_day='08:00:00', start_date='2024-08-20')
        db.session.add(habit)
        habit2 = Habit(user_id=self.user.id, name='Reading', frequency='Daily', time_of_day='09:00:00', start_date='2024-08-20')
        db.session.add(habit2)
        db.session.commit()
        
        response = self.client.get('/habits')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(2, len(data['habits']))
        self.assertIn('Exercise', str(response.data))
        self.assertIn('08:00:00', str(response.data))
        self.assertIn('Reading', str(response.data))
        self.assertIn('09:00:00', str(response.data))

    def test_get_habit(self):
        habit = Habit(user_id=self.user.id, name='Exercise', frequency='Daily', time_of_day='08:00:00', start_date='2024-08-20')
        db.session.add(habit)
        db.session.commit()

        response = self.client.get(f'/habits/{habit.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Exercise', str(response.data))

    def test_update_habit(self):
        habit = Habit(user_id=self.user.id, name='Exercise', frequency='Daily', time_of_day='08:00:00', start_date='2024-08-20')
        db.session.add(habit)
        db.session.commit()
        response = self.client.put(f'/habits/{habit.id}', json={
            'name': 'Updated Habit',
            'frequency': 'Weekly',
            'time_of_day': '08:00:00'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Updated Habit', str(response.data))
        self.assertIn('Weekly', str(response.data))

    def test_delete_habit(self):
        habit = Habit(user_id=self.user.id, name='Exercise', frequency='Daily', time_of_day='08:00:00', start_date='2024-08-20')
        db.session.add(habit)
        db.session.commit()
        response = self.client.delete(f'/habits/{habit.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'Habit - {habit.name} - deleted', str(response.data))


if __name__ == '__main__':
    unittest.main()
