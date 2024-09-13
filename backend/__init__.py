from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()

login_manager.login_view = 'auth.login'
login_manager.session_protection = "strong"

def create_app():
    # Create Flask app instance
    app = Flask(__name__,
                static_folder='../frontend/build',  # Serve React static files
                template_folder='../frontend/build')

    # Load configuration from Config class
    app.config.from_object('backend.config.Config')

    # Initialize extensions
    db.init_app(app)
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
        """
        Serve the React frontend for any non-API route.
        All frontend routing will be handled by React Router.
        """
        if path != '' and os.path.exists(app.static_folder + '/' + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    # User loader for Flask-Login
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Ensure the app context is available and tables are created (for development)
    with app.app_context():
        db.create_all()

    return app
