from flask import Blueprint, request, jsonify, send_from_directory, render_template, current_app
from backend.models import db, Recipe, Rating, Inventory
import openai
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
    user_id = data.get('user_id')

    # Passively encourage the addition of dark leafy greens
    if 'spinach' not in ingredients and 'kale' not in ingredients:
        ingredients += ", spinach, kale"

    # Search for an existing recipe that matches the ingredients and is high in nutrition
    existing_recipe = Recipe.query.filter(
        Recipe.ingredients.contains(ingredients)
    ).order_by(
        Recipe.nutrition_score.desc(),
        Recipe.fiber_content.desc(),
        Recipe.sugar_content.asc()
    ).first()

    if existing_recipe:
        return jsonify({
            "title": existing_recipe.title,
            "recipe": existing_recipe.instructions,
            "average_rating": existing_recipe.average_rating(),
            "fiber_content": existing_recipe.fiber_content,
            "sugar_content": existing_recipe.sugar_content,
            "nutrition_score": existing_recipe.nutrition_score
        })

    # If no existing recipe matches, generate a new one using OpenAI
    recipe = generate_recipe(ingredients, mood)
    return jsonify({"recipe": recipe})

@main_blueprint.route('/save-recipe', methods=['POST'])
def save_recipe():
    data = request.json
    new_recipe = Recipe(
        title=data.get('title'),
        ingredients=data.get('ingredients'),
        instructions=data.get('instructions'),
        fiber_content=data.get('fiber_content'),
        sugar_content=data.get('sugar_content'),
        nutrition_score=data.get('nutrition_score'),
        user_id=data.get('user_id')  # Optional, since recipes are shared
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({"message": "Recipe saved successfully!"})

@main_blueprint.route('/get-recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.order_by(
        Recipe.nutrition_score.desc(),
        Recipe.fiber_content.desc(),
        Recipe.sugar_content.asc()
    ).all()
    return jsonify([{
        "title": recipe.title,
        "ingredients": recipe.ingredients,
        "instructions": recipe.instructions,
        "average_rating": recipe.average_rating(),
        "fiber_content": recipe.fiber_content,
        "sugar_content": recipe.sugar_content,
        "nutrition_score": recipe.nutrition_score
    } for recipe in recipes])

@main_blueprint.route('/rate-recipe', methods=['POST'])
def rate_recipe():
    data = request.json
    recipe_id = data.get('recipe_id')
    user_id = data.get('user_id')
    score = data.get('score')

    if not 1 <= score <= 5:
        return jsonify({"error": "Rating must be between 1 and 5"}), 400

    rating = Rating.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if rating:
        # Update the existing rating
        rating.score = score
    else:
        # Create a new rating
        rating = Rating(score=score, user_id=user_id, recipe_id=recipe_id)
        db.session.add(rating)
    
    db.session.commit()
    return jsonify({"message": "Rating submitted successfully!"})

@main_blueprint.route('/update-inventory', methods=['POST'])
def update_inventory():
    data = request.json
    user_id = data.get('user_id')
    ingredients = data.get('ingredients')

    for ingredient in ingredients:
        existing_ingredient = Inventory.query.filter_by(user_id=user_id, ingredient=ingredient).first()
        if existing_ingredient:
            # Optionally update the quantity if needed
            pass
        else:
            new_inventory_item = Inventory(ingredient=ingredient, user_id=user_id)
            db.session.add(new_inventory_item)

    db.session.commit()
    return jsonify({"message": "Inventory updated successfully!"})

def generate_recipe(ingredients, mood):
    prompt = f"I have the following ingredients: {ingredients}. I'm in the mood for something {mood} that is high in nutrition, high in fiber, and low in sugar. What can I cook?"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200
    )
    return response.choices[0].text.strip()

@main_blueprint.route('/', defaults={'path': ''})
@main_blueprint.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(current_app.static_folder, path)):
        return send_from_directory(current_app.static_folder, path)
    else:
        return send_from_directory(current_app.template_folder, 'index.html')



