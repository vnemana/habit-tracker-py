from .db import db
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime

# Define the enum type for frequency
frequency_enum = ENUM('Daily', 'Weekly', 'Monthly', 'Yearly', name='frequency_enum', create_type=False)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    # Define a relationship to the Habit table
    habits = db.relationship('Habit', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Habit(db.Model):
    __tablename__ = 'habits'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    frequency = db.Column(db.String(50), nullable=False)
    time_of_day = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Habit {self.name}>'
