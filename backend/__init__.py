# backend/__init__.py

from flask import Flask
from .config import Config
from .models import db, User
from flask_login import LoginManager
from .auth import auth_blueprint
from .routes import main_blueprint

def create_app():
    app = Flask(
        __name__,
        static_folder='../frontend/build',  # Set the static folder to the build directory
        template_folder='../frontend/build'  # Set the template folder to the build directory
    )
    app.config.from_object(Config)
    
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)

    return app
