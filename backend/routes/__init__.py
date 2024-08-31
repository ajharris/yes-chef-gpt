from flask import Flask
from backend.routes.recipes import recipes_blueprint
from backend.routes.ratings import ratings_blueprint
from backend.routes.inventory import inventory_blueprint
from backend.routes.main import main_blueprint

def create_app():
    app = Flask(
        __name__,
        static_folder='../frontend/build', 
        template_folder='../frontend/build'
    )

    # Register Blueprints
    app.register_blueprint(recipes_blueprint, url_prefix='/api/recipes')
    app.register_blueprint(ratings_blueprint, url_prefix='/api/ratings')
    app.register_blueprint(inventory_blueprint, url_prefix='/api/inventory')
    app.register_blueprint(main_blueprint)

    return app
