from flask import Flask
from .config import DevelopmentConfig, TestingConfig
from .db import db, migrate

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints or import views here
    from .models import User, Habit

    # Import and register blueprints
    from .routes.user_routes import user_bp
    from .routes.habit_routes import habit_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(habit_bp)

    return app
