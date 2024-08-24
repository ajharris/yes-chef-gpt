from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_socketio import emit
from backend.models import db, Recipe, Rating, Inventory
from . import socketio
import os

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/about')
def about():
    return "About ChefGPT"

@main_blueprint.route('/generate-recipe', methods=['POST'])
def generate_recipe_route():
    data = request.json
    ingredients = data.get('ingredients')
    mood = data.get('mood')
    recipe = "Recipe based on ingredients: " + ingredients + " and mood: " + mood
    return jsonify({"recipe": recipe})

@main_blueprint.route('/save-recipe', methods=['POST'])
def save_recipe():
    data = request.json
    new_recipe = Recipe(
        title=data['title'],
        ingredients=data['ingredients'],
        instructions=data['instructions'],
        user_id=data.get('user_id')
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({"message": "Recipe saved successfully!"})

@main_blueprint.route('/get-recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify([{"title": r.title, "ingredients": r.ingredients, "instructions": r.instructions} for r in recipes])

@main_blueprint.route('/rate-recipe', methods=['POST'])
def rate_recipe():
    data = request.json
    rating = Rating(
        score=data['score'],
        user_id=data['user_id'],
        recipe_id=data['recipe_id']
    )
    db.session.add(rating)
    db.session.commit()
    return jsonify({"message": "Rating submitted successfully!"})

@main_blueprint.route('/update-inventory', methods=['POST'])
def update_inventory():
    data = request.json
    user_id = data['user_id']
    ingredients = data['ingredients']
    for ingredient in ingredients:
        inventory_item = Inventory(user_id=user_id, ingredient=ingredient)
        db.session.add(inventory_item)
    db.session.commit()
    return jsonify({"message": "Inventory updated successfully!"})

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
    emit('button_click_response', {'message': 'Button was clicked!', 'status': 'success'})
