from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from backend.models import Inventory
from backend.extensions import db

inventory_blueprint = Blueprint('inventory', __name__)

@inventory_blueprint.route('/inventory', methods=['GET'])
@login_required
def get_inventory():
    items = Inventory.query.filter_by(user_id=current_user.id).all()
    return jsonify([item.serialize() for item in items])

@inventory_blueprint.route('/inventory', methods=['POST'])
@login_required
def add_inventory():
    data = request.get_json()
    new_item = Inventory(
        user_id=current_user.id,
        ingredient=data['ingredient'],
        quantity=data['quantity'],
        unit=data['unit']
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.serialize()), 201
