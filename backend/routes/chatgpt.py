import openai
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import logging
from backend.models import Recipe
from backend.extensions import db

# For testing purposes, override the login_required decorator
import os
if os.getenv('FLASK_ENV') == 'testing':
    from flask_login import login_required
    def login_required(func):
        return func

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

chatgpt_blueprint = Blueprint('chatgpt', __name__)

@chatgpt_blueprint.route('/suggest_recipes', methods=['POST'])
def suggest_recipes():
    logger.error(f"Database tables: {db.metadata.tables.keys()}")  # Log database tables

    data = request.get_json()

    # Validate input
    if not data or 'ingredients' not in data:
        return jsonify({'error': 'Missing ingredients field'}), 400

    ingredients = data.get('ingredients')
    dietary_restrictions = data.get('dietary_restrictions')

    # Handle anonymous and logged-in users
    if dietary_restrictions is None and hasattr(current_user, 'dietary_preferences'):
        dietary_restrictions = current_user.dietary_preferences
    dietary_restrictions = dietary_restrictions or []

    # Input validation: ingredients must be a list of strings
    if not isinstance(ingredients, list) or not all(isinstance(i, str) for i in ingredients):
        return jsonify({"error": "Ingredients must be a list of strings"}), 422

    # Check for existing recipe in the database
    existing_recipe = Recipe.query.filter_by(raw_ingredients=ingredients).first()
    if existing_recipe:
        return jsonify({
            "recipe": {
                "ingredients": existing_recipe.ingredients,
                "preparation": existing_recipe.preparation,
                "pickup": existing_recipe.pickup
            }
        }), 200

    # Generate recipe suggestions (mocked for now)
    prompt = f"Suggest recipes using the following ingredients: {', '.join(ingredients)}."
    if dietary_restrictions:
        prompt += f" Consider these dietary restrictions: {', '.join(dietary_restrictions)}."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that suggests recipes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        suggestions = response['choices'][0]['message']['content']
        # If suggestions is a JSON string, parse it
        import json
        if isinstance(suggestions, str):
            try:
                parsed = json.loads(suggestions)
                # If the parsed object is a dict with 'recipes' key, return as is
                if isinstance(parsed, dict) and "recipes" in parsed:
                    return jsonify(parsed), 200
                # If parsed is a recipe dict, return as recipe
                if isinstance(parsed, dict):
                    return jsonify({"recipe": parsed}), 200
            except Exception:
                pass
            # Otherwise, treat as plain text
            lines = suggestions.strip().split("\n")
        elif isinstance(suggestions, dict):
            # If already a dict, return as recipe
            return jsonify({"recipe": suggestions}), 200
        else:
            lines = str(suggestions).strip().split("\n")

        # Robust parsing for both real and mocked responses
        try:
            prep_idx = lines.index("Preparation:")
            pickup_idx = lines.index("Pickup:")
            ingredients = lines[1:prep_idx]
            preparation = lines[prep_idx + 1:pickup_idx]
            pickup = lines[pickup_idx + 1:]
        except ValueError:
            # Fallback for mocked/simple responses
            ingredients = []
            preparation = []
            pickup = []
            for line in lines:
                if line.startswith("Ingredients:"):
                    ingredients.append(line.replace("Ingredients:", "").strip())
                elif line.startswith("Preparation:"):
                    preparation.append(line.replace("Preparation:", "").strip())
                elif line.startswith("Pickup:"):
                    pickup.append(line.replace("Pickup:", "").strip())
                elif line:
                    # If line doesn't match, add to ingredients by default
                    ingredients.append(line.strip())
        # Save the new recipe to the database
        new_recipe = Recipe(
            title="Suggested Recipe",
            ingredients=", ".join(ingredients),
            instructions="",
            preparation="\n".join(preparation),
            pickup="\n".join(pickup),
            raw_ingredients=ingredients
        )
        db.session.add(new_recipe)
        db.session.commit()
        return jsonify({
            "recipe": {
                "ingredients": new_recipe.ingredients,
                "preparation": new_recipe.preparation,
                "pickup": new_recipe.pickup
            }
        }), 200

    except Exception as e:
        logger.error("Error generating recipes: %s", str(e))
        return jsonify({'error': 'Failed to generate recipes', 'details': str(e)}), 500
