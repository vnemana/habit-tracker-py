from flask import Flask
from .config import Config
from .db import db, migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints or import views here
    from .models import User, Habit

    @app.route('/')
    def home():
        return "Hello, Flask with PostgreSQL!"

    return app
