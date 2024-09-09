from flask import Blueprint, request, jsonify

inventory_blueprint = Blueprint('inventory', __name__)

# Get all inventory items
@inventory_blueprint.route('/', methods=['GET'])
def get_inventory():
    from backend import db
    from backend.models import InventoryItem  # Import models inside the function

    inventory_items = InventoryItem.query.all()
    item_list = [{"id": item.id, "name": item.name, "quantity": item.quantity} for item in inventory_items]
    return jsonify(item_list), 200

# Add a new inventory item
@inventory_blueprint.route('/', methods=['POST'])
def add_inventory_item():
    from backend import db
    from backend.models import InventoryItem

    data = request.json
    name = data.get('name')
    quantity = data.get('quantity')

    new_item = InventoryItem(name=name, quantity=quantity)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({"message": "Item added to inventory"}), 201

# Update an inventory item
@inventory_blueprint.route('/<int:item_id>', methods=['PUT'])
def update_inventory_item(item_id):
    from backend import db
    from backend.models import InventoryItem

    item = InventoryItem.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.json
    item.name = data.get('name')
    item.quantity = data.get('quantity')

    db.session.commit()

    return jsonify({"message": "Inventory item updated"}), 200
