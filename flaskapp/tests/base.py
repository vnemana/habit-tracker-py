import unittest
from flaskapp import create_app
from flaskapp.db import db
from flaskapp.config import TestingConfig

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_class=TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
