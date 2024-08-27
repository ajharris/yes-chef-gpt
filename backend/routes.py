from flask import Blueprint, request, jsonify, send_from_directory, current_app, abort
from backend.models import db, Recipe, Rating, Inventory
import os

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/api/server-info', methods=['GET'])
def server_info():
    info = {
        "server_name": "ChefGPT",
        "version": "1.0.0",
        "status": "Running"
    }
    return jsonify(info)

@main_blueprint.route('/about')
def about():
    return "About ChefGPT"

@main_blueprint.route('/generate-recipe', methods=['POST'])
def generate_recipe_route():
    data = request.json
    ingredients = data.get('ingredients')
    mood = data.get('mood')
    if not ingredients or not mood:
        abort(400, description="Missing required ingredients or mood")
    recipe = "Recipe based on ingredients: " + ingredients + " and mood: " + mood
    return jsonify({"recipe": recipe})

@main_blueprint.route('/save-recipe', methods=['POST'])
def save_recipe():
    try:
        data = request.json
        title = data.get('title')
        ingredients = data.get('ingredients')
        instructions = data.get('instructions')
        user_id = data.get('user_id')

        if not title or not ingredients or not instructions:
            abort(400, description="Missing required fields")

        new_recipe = Recipe(
            title=title,
            ingredients=ingredients,
            instructions=instructions,
            user_id=user_id
        )
        db.session.add(new_recipe)
        db.session.commit()
        return jsonify({"message": "Recipe saved successfully!"})
    except Exception as e:
        return jsonify({"error": "Unable to save recipe due to an error: {}".format(e)}), 500

@main_blueprint.route('/get-recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify([{"title": r.title, "ingredients": r.ingredients, "instructions": r.instructions} for r in recipes])

@main_blueprint.route('/rate-recipe', methods=['POST'])
def rate_recipe():
    data = request.json
    score = data.get('score')
    user_id = data.get('user_id')
    recipe_id = data.get('recipe_id')

    if not 1 <= score <= 5:
        return jsonify({"error": "Rating must be between 1 and 5"}), 400

    rating = Rating(
        score=score,
        user_id=user_id,
        recipe_id=recipe_id
    )
    db.session.add(rating)
    db.session.commit()
    return jsonify({"message": "Rating submitted successfully!"})

@main_blueprint.route('/update-inventory', methods=['POST'])
def update_inventory():
    data = request.json
    user_id = data.get('user_id')
    ingredients = data.get('ingredients')

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
