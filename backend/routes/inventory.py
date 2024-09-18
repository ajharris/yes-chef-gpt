from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from backend.models import Inventory
from backend.extensions import db

inventory_blueprint = Blueprint('inventory', __name__)

# Get user's inventory
@inventory_blueprint.route('/inventory', methods=['GET'])
@login_required
def get_inventory():
    items = Inventory.query.filter_by(user_id=current_user.id).all()
    return jsonify([item.serialize() for item in items]), 200

# Add an item to the inventory
@inventory_blueprint.route('/inventory', methods=['POST'])
@login_required
def add_inventory():
    data = request.get_json()

    # Validate required 'ingredient' field
    if 'ingredient' not in data:
        return jsonify({'error': 'Missing required field: ingredient'}), 400

    try:
        new_item = Inventory(
            user_id=current_user.id,
            ingredient=data['ingredient'],
            quantity=data.get('quantity'),  # Can be None
            unit=data.get('unit')  # Can be None
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify(new_item.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update inventory item
@inventory_blueprint.route('/inventory/<int:item_id>', methods=['PUT'])
@login_required
def update_inventory(item_id):
    data = request.get_json()

    try:
        item = Inventory.query.filter_by(id=item_id, user_id=current_user.id).first()
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        
        # Update fields if provided
        if 'ingredient' in data:
            item.ingredient = data['ingredient']
        if 'quantity' in data:
            item.quantity = data.get('quantity')  # Can be None
        if 'unit' in data:
            item.unit = data.get('unit')  # Can be None

        db.session.commit()
        return jsonify(item.serialize()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete inventory item
@inventory_blueprint.route('/inventory/<int:item_id>', methods=['DELETE'])
@login_required
def delete_inventory(item_id):
    try:
        item = Inventory.query.filter_by(id=item_id, user_id=current_user.id).first()
        if not item:
            return jsonify({'error': 'Item not found'}), 404

        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Check ingredient availability against a recipe
def check_ingredient_availability(user_inventory, recipe_ingredient):
    # If no quantity or unit is provided, ask the user if they have enough
    if user_inventory.quantity is None or user_inventory.unit is None:
        return f"Do you have enough {recipe_ingredient.name}? (Currently unspecified in your inventory)"
    
    # Otherwise, compare the available amount with the recipe's required amount
    if user_inventory.quantity >= recipe_ingredient.required_quantity:
        return "You have enough!"
    else:
        return f"You need {recipe_ingredient.required_quantity} {recipe_ingredient.unit} of {recipe_ingredient.name}, but you only have {user_inventory.quantity} {user_inventory.unit}."
