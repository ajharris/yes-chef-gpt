from flask import Blueprint, request, jsonify

ratings_blueprint = Blueprint('ratings', __name__)

# Get all ratings for a recipe
@ratings_blueprint.route('/<int:recipe_id>', methods=['GET'])
def get_ratings(recipe_id):
    from backend import db
    from backend.models import Rating, Recipe  # Import models inside the function

    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    ratings = Rating.query.filter_by(recipe_id=recipe_id).all()
    rating_list = [{"id": rating.id, "rating": rating.rating, "comment": rating.comment} for rating in ratings]
    return jsonify(rating_list), 200

# Create a new rating
@ratings_blueprint.route('/<int:recipe_id>', methods=['POST'])
def create_rating(recipe_id):
    from backend import db
    from backend.models import Rating, Recipe

    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    data = request.json
    rating = data.get('rating')
    comment = data.get('comment')

    new_rating = Rating(recipe_id=recipe_id, rating=rating, comment=comment)
    db.session.add(new_rating)
    db.session.commit()

    return jsonify({"message": "Rating created successfully"}), 201
