import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('HABITS_POSTGRES_URI')
    SQLALCHEMY_TRACK_NOTIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://test_user:test_password@localhost:5435/test_db'

# class ProductionConfig(Config):
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://prod_user:prod_password@localhost/prod_db')
#     DEBUG = False
#     TESTING = False