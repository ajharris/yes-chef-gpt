import openai
from flask import Blueprint, request, jsonify
from flask_login import login_required
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

chatgpt_blueprint = Blueprint('chatgpt', __name__)

@chatgpt_blueprint.route('/api/suggest_recipes', methods=['POST'])
@login_required
def suggest_recipes():
    data = request.get_json()

    # Validate input
    if not data or 'ingredients' not in data:
        return jsonify({'error': 'Missing ingredients field'}), 400

    ingredients = data.get('ingredients')
    dietary_restrictions = data.get('dietary_restrictions', [])

    if not isinstance(ingredients, list) or not all(isinstance(i, str) for i in ingredients):
        return jsonify({'error': 'Ingredients must be a list of strings'}), 422

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
        suggestions = response['choices'][0]['message']['content'].strip().split('\n')

        # Remove duplicates and return suggestions
        unique_suggestions = list(set(suggestions))
        return jsonify({'recipes': unique_suggestions}), 200

    except Exception as e:
        logger.error("Error generating recipes: %s", str(e))
        return jsonify({'error': 'Failed to generate recipes', 'details': str(e)}), 500
