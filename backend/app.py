from dotenv import load_dotenv
load_dotenv()  # This will load the .env file at the application startup

from flask import Flask
from .config import Config
from .models import db
from .routes import main_blueprint

app = Flask(__name__, static_folder='../frontend/build', template_folder='../frontend/build')
app.config.from_object(Config)
db.init_app(app)
app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
