from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from backend.models import Rating
from backend.extensions import db

ratings_blueprint = Blueprint('ratings', __name__)

@ratings_blueprint.route('/ratings', methods=['POST'])
@login_required
def add_rating():
    data = request.get_json()
    new_rating = Rating(
        user_id=current_user.id,
        recipe_id=data['recipe_id'],
        score=data['score']
    )
    db.session.add(new_rating)
    db.session.commit()
    return jsonify(new_rating.serialize()), 201
