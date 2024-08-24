# backend/__init__.py

from flask import Flask
from .config import Config
from .models import db, User
from flask_login import LoginManager
from .auth import auth_blueprint  # Ensure this blueprint is properly defined in your project
from .routes import main_blueprint

def create_app():
    app = Flask(
        __name__,
        static_folder='../frontend/build',  # Set the static folder to the build directory
        template_folder='../frontend/build'  # Set the template folder to the build directory
    )
    
    # Load configuration from 'config.py'
    app.config.from_object(Config)
    
    # Initialize the database connection
    db.init_app(app)

    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Define the endpoint for unauthorized users
    login_manager.init_app(app)

    # User loader callback for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Fetch the user by ID

    with app.app_context():
        db.create_all()  # Create database tables for all models

    # Register blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint, url_prefix='/api')

    return app
