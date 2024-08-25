from flask import Flask
from .config import Config
from .models import db, User
from flask_login import LoginManager
from .auth import auth_blueprint
from .routes import main_blueprint
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app():
    app = Flask(
        __name__,
        static_folder='../frontend/build', 
        template_folder='../frontend/build'
    )
    app.config.from_object(Config)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    socketio.init_app(app, cors_allowed_origins="*")

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app)
