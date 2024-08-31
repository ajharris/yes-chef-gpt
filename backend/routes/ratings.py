from flask import Blueprint, request, jsonify
from backend.models import db, Rating

ratings_blueprint = Blueprint('ratings', __name__)

@ratings_blueprint.route('/rate-recipe', methods=['POST'])
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
