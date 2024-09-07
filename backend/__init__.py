from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS  # For handling CORS issues with the frontend
import os

# Load environment variables from a .env file if it exists
load_dotenv()

# Initialize extensions without passing the app yet
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Initialize the login view
login_manager.login_view = 'auth.login'  # Redirect to the login page for protected routes


def create_app():
    # Create Flask app instance
    app = Flask(
        __name__,
        static_folder='../frontend/build',  # Serve React static files
        template_folder='../frontend/build'  # Use React build folder for templates
    )

    # Load configuration from the Config object
    app.config.from_object('backend.config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Enable CORS (optional but recommended if React frontend makes API requests)
    CORS(app)

    # Import and register blueprints
    from .auth import auth_blueprint
    from .routes.recipes import recipes_blueprint
    from .routes.ratings import ratings_blueprint
    from .routes.inventory import inventory_blueprint
    from .routes.main import main_blueprint

    # Register API Blueprints with their URL prefixes
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(recipes_blueprint, url_prefix='/api/recipes')
    app.register_blueprint(ratings_blueprint, url_prefix='/api/ratings')
    app.register_blueprint(inventory_blueprint, url_prefix='/api/inventory')
    app.register_blueprint(main_blueprint)  # No URL prefix for the main blueprint

    # Serve React frontend from the build folder for all unmatched routes
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react_app(path):
        """
        Serve the React frontend for any non-API route.
        All frontend routing will be handled by React Router.
        """
        if path != '' and os.path.exists(app.static_folder + '/' + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    # User loader for Flask-Login (to load user by ID)
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Optionally create the database tables (for development)
    with app.app_context():
        db.create_all()

    return app
