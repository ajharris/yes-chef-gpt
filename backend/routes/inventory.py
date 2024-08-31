from flask import Blueprint, request, jsonify
from backend.models import db, Inventory

inventory_blueprint = Blueprint('inventory', __name__)

@inventory_blueprint.route('/update-inventory', methods=['POST'])
def update_inventory():
    data = request.json
    user_id = data.get('user_id')
    ingredients = data.get('ingredients')

    for ingredient in ingredients:
        inventory_item = Inventory(user_id=user_id, ingredient=ingredient)
        db.session.add(inventory_item)
    db.session.commit()
    return jsonify({"message": "Inventory updated successfully!"})
