from .db import db
from sqlalchemy.dialects.postgresql import ENUM

# Define the enum type for frequency
frequency_enum = ENUM('Daily', 'Weekly', 'Monthly', 'Yearly', name='frequency_enum', create_type=False)
auth_provider_enum = ENUM('Google', 'Facebook', 'Github', name='auth_provider_enum', create_type=False)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    auth_provider = db.Column(
        ENUM('google', 'facebook', 'github', name='auth_provider_enum'),
        nullable=False
    )
    provider_id = db.Column(db.String(100), nullable=False)
    
    # Unique constraint on the combination of auth_provider and provider_id
    __table_args__ = (db.UniqueConstraint('auth_provider', 'provider_id', name='uq_auth_provider_provider_id'),)

    # Define a relationship to the Habit table
    habits = db.relationship('Habit', backref='user', lazy=True)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}', auth_provider='{self.auth_provider}', provider_id='{self.provider_id}')>"

class Habit(db.Model):
    __tablename__ = 'habits'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    frequency = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    time_of_day = db.Column(db.Time, nullable=False)
    
    def __repr__(self):
        return f'<Habit {self.name}>'
