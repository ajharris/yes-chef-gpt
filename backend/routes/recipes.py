from flask import Blueprint, request, jsonify

recipes_blueprint = Blueprint('recipes', __name__)

# Get all recipes
@recipes_blueprint.route('/', methods=['GET'])
def get_all_recipes():
    from backend import db
    from backend.models import Recipe  # Import models inside the function

    recipes = Recipe.query.all()
    recipe_list = [{"id": recipe.id, "name": recipe.name, "ingredients": recipe.ingredients} for recipe in recipes]
    return jsonify(recipe_list), 200

# Create a new recipe
@recipes_blueprint.route('/', methods=['POST'])
def create_recipe():
    from backend import db
    from backend.models import Recipe

    data = request.json
    name = data.get('name')
    ingredients = data.get('ingredients')

    new_recipe = Recipe(name=name, ingredients=ingredients)
    db.session.add(new_recipe)
    db.session.commit()

    return jsonify({"message": "Recipe created successfully"}), 201

# Delete a recipe
@recipes_blueprint.route('/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    from backend import db
    from backend.models import Recipe

    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    db.session.delete(recipe)
    db.session.commit()

    return jsonify({"message": "Recipe deleted successfully"}), 200
