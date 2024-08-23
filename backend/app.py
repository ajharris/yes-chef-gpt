from flask import Flask
from backend.config import Config
from backend.models import db
from backend.routes import main_blueprint


app = Flask(__name__, static_folder='../frontend/build', template_folder='../frontend/build')


app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
                                                                            