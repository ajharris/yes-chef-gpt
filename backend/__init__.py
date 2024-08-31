from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Load environment variables from a .env file if it exists
load_dotenv()

# Initialize the database
db = SQLAlchemy()
migrate = Migrate()

# Initialize the login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Redirect to the login page for protected routes

def create_app():
    app = Flask(
        __name__,
        static_folder='../frontend/build', 
        template_folder='../frontend/build'
    )

    # Load configuration from object
    app.config.from_object('backend.config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import and register Blueprints
    from .auth import auth_blueprint
    from .routes.recipes import recipes_blueprint
    from .routes.ratings import ratings_blueprint
    from .routes.inventory import inventory_blueprint
    from .routes.main import main_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(recipes_blueprint, url_prefix='/api/recipes')
    app.register_blueprint(ratings_blueprint, url_prefix='/api/ratings')
    app.register_blueprint(inventory_blueprint, url_prefix='/api/inventory')
    app.register_blueprint(main_blueprint)  # No URL prefix for main

    # Load user callback for Flask-Login
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Optionally, create the database tables if they don't exist (useful for development)
    with app.app_context():
        db.create_all()

    return app
