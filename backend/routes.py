from flask import Blueprint, request, jsonify, send_from_directory, render_template, current_app
from backend.models import db, Recipe, Rating, Inventory
from flask_socketio import SocketIO, emit
import openai
import os

main_blueprint = Blueprint('main', __name__)
socketio = SocketIO()

@main_blueprint.route('/about')
def about():
    return "About ChefGPT"

@main_blueprint.route('/generate-recipe', methods=['POST'])
def generate_recipe_route():
    # Your existing code here...

@main_blueprint.route('/save-recipe', methods=['POST'])
def save_recipe():
    # Your existing code here...

@main_blueprint.route('/get-recipes', methods=['GET'])
def get_recipes():
    # Your existing code here...

@main_blueprint.route('/rate-recipe', methods=['POST'])
def rate_recipe():
    # Your existing code here...

@main_blueprint.route('/update-inventory', methods=['POST'])
def update_inventory():
    # Your existing code here...

@main_blueprint.route('/', defaults={'path': ''})
@main_blueprint.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(current_app.static_folder, path)):
        return send_from_directory(current_app.static_folder, path)
    else:
        return send_from_directory(current_app.template_folder, 'index.html')

# SocketIO event handlers
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('button_click')
def handle_button_click(data):
    print('Button click received:', data)
    # Process the button click here
    emit('button_click_response', {'message': 'Button was clicked!', 'status': 'success'})

def create_app():
    app = Flask(
        __name__,
        static_folder='../frontend/build',
        template_folder='../frontend/build'
    )
    app.config.from_object(Config)
    db.init_app(app)
    socketio.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(main_blueprint)
    return app
