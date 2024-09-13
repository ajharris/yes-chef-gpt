from flask import Blueprint, request, jsonify
from flask_login import login_required
from backend.models import Recipe
from backend.extensions import db

recipes_blueprint = Blueprint('recipes', __name__)

@recipes_blueprint.route('/recipes', methods=['GET'])
@login_required
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify([recipe.serialize() for recipe in recipes])

@recipes_blueprint.route('/recipes', methods=['POST'])
@login_required
def generate_recipe():
    data = request.get_json()
    # Logic to generate recipe goes here
    return jsonify({"message": "Recipe generated"})
