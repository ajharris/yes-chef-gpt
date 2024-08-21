from flask import request, jsonify
from app import app, db
from models import User, Recipe

@app.route('/generate-recipe', methods=['POST'])
def generate_recipe_route():
    data = request.json
    ingredients = data.get('ingredients')
    mood = data.get('mood')
    # Call the OpenAI API (you'll need to implement this)
    recipe = generate_recipe(ingredients, mood)
    return jsonify({"recipe": recipe})

@app.route('/save-recipe', methods=['POST'])
def save_recipe():
    data = request.json
    new_recipe = Recipe(
        title=data.get('title'),
        ingredients=data.get('ingredients'),
        instructions=data.get('instructions'),
        user_id=data.get('user_id')
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({"message": "Recipe saved successfully!"})

@app.route('/get-recipes', methods=['GET'])
def get_recipes():
    user_id = request.args.get('user_id')
    recipes = Recipe.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "title": recipe.title,
        "ingredients": recipe.ingredients,
        "instructions": recipe.instructions
    } for recipe in recipes])


import openai

openai.api_key = 'your-openai-api-key'

def generate_recipe(ingredients, mood):
    prompt = f"I have the following ingredients: {ingredients}. I'm in the mood for something {mood}. What can I cook?"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200
    )
    return response.choices[0].text.strip()
