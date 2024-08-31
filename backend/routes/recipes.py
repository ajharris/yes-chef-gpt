from flask import Blueprint, request, jsonify, abort
from backend.models import db, Recipe

recipes_blueprint = Blueprint('recipes', __name__)

@recipes_blueprint.route('/generate-recipe', methods=['POST'])
def generate_recipe_route():
    data = request.json
    ingredients = data.get('ingredients')
    mood = data.get('mood')
    if not ingredients or not mood:
        abort(400, description="Missing required ingredients or mood")
    recipe = "Recipe based on ingredients: " + ingredients + " and mood: " + mood
    return jsonify({"recipe": recipe})

@recipes_blueprint.route('/save-recipe', methods=['POST'])
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

@recipes_blueprint.route('/get-recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify([{"title": r.title, "ingredients": r.ingredients, "instructions": r.instructions} for r in recipes])
