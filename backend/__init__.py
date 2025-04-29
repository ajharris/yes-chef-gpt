# backend/__init__.py

from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Import extensions
from .extensions import db, bcrypt, migrate, login_manager

# Load environment variables from a .env file
load_dotenv()

# Example: Accessing an environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Log the status of the OPENAI_API_KEY
if OPENAI_API_KEY:
    print("OPENAI_API_KEY successfully loaded.")
else:
    print("Warning: OPENAI_API_KEY is not set.")

def create_app(config_class='backend.config.Config'):
    # Create Flask app instance
    app = Flask(__name__,
                static_folder='../frontend/build',
                template_folder='../frontend/build')

    # Load configuration
    app.config.from_object(config_class)

    # Initialize extensions with the app
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Ensure tables are created during app initialization

    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Enable CORS
    CORS(app)

    # Import and register blueprints
    from .routes.auth import auth_blueprint
    from .routes.recipes import recipes_blueprint
    from .routes.ratings import ratings_blueprint
    from .routes.inventory import inventory_blueprint
    from .routes.chatgpt import chatgpt_blueprint
    from .routes.main import main_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(recipes_blueprint, url_prefix='/api/recipes')
    app.register_blueprint(ratings_blueprint, url_prefix='/api/ratings')
    app.register_blueprint(inventory_blueprint, url_prefix='/api/inventory')
    app.register_blueprint(chatgpt_blueprint, url_prefix='/api')
    app.register_blueprint(main_blueprint)

    # Serve React frontend for non-API routes
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react_app(path):
        if path != '' and os.path.exists(app.static_folder + '/' + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    # User loader for Flask-Login
    from .models import User, Recipe, Rating, Inventory  # Ensure all models are imported
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
