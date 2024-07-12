import unittest
from flaskapp import db
from flaskapp.models import User, Habit
from tests.base import BaseTestCase

class HabitModelTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Ensure a user is created for the habit dependency
        self.user = User(username='testuser', password='password')
        db.session.add(self.user)
        db.session.commit()
    
    def test_create_habit(self):
        habit = Habit(user_id=self.user.id, name='Exercise', frequency='Daily', time_of_day=None)
        db.session.add(habit)
        db.session.commit()

        queried_habit = Habit.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(queried_habit)
        self.assertEqual(queried_habit.name, 'Exercise')

if __name__ == '__main__':
    unittest.main()
