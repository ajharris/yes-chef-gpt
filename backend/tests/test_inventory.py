import pytest
from flask import jsonify
from backend.models import Inventory
from backend.extensions import db
from flask_login import login_user
from backend.models import User

@pytest.fixture
def test_user():
    # Creating a test user and setting the password correctly
    user = User(username='testuser', email='testuser@example.com')
    user.set_password('testpassword')  # Assuming your User model has a set_password method
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def logged_in_user(client, test_user):
    # Logs in the user
    with client.session_transaction() as session:
        login_user(test_user)
    yield test_user

def test_get_inventory(client, logged_in_user):
    # Test case for getting inventory
    response = client.get('/inventory')
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Response should be a list

def test_add_inventory(client, logged_in_user):
    # Test case for adding inventory
    data = {
        'ingredient': 'Tomato',
        'quantity': 3,
        'unit': 'kg'
    }
    response = client.post('/inventory', json=data)
    assert response.status_code == 201
    assert 'ingredient' in response.json
    assert response.json['ingredient'] == 'Tomato'

def test_add_inventory_missing_fields(client, logged_in_user):
    # Test case for missing fields in the POST request
    data = {
        'ingredient': 'Tomato'
        # Missing 'quantity' and 'unit'
    }
    response = client.post('/inventory', json=data)
    assert response.status_code == 400  # Expecting bad request due to missing fields
    assert 'error' in response.json

def test_update_inventory(client, logged_in_user):
    # First, add an inventory item to update
    new_item = Inventory(user_id=logged_in_user.id, ingredient='Apple', quantity=5, unit='kg')
    db.session.add(new_item)
    db.session.commit()

    # Now test updating it
    update_data = {
        'quantity': 10,
        'unit': 'lbs'
    }
    response = client.put(f'/inventory/{new_item.id}', json=update_data)
    assert response.status_code == 200
    assert response.json['quantity'] == 10
    assert response.json['unit'] == 'lbs'

def test_update_inventory_not_found(client, logged_in_user):
    # Test case for updating a non-existent inventory item
    update_data = {
        'quantity': 10,
        'unit': 'lbs'
    }
    response = client.put('/inventory/99999', json=update_data)  # Use an invalid ID
    assert response.status_code == 404
    assert 'error' in response.json

def test_delete_inventory(client, logged_in_user):
    # First, add an inventory item to delete
    new_item = Inventory(user_id=logged_in_user.id, ingredient='Banana', quantity=2, unit='kg')
    db.session.add(new_item)
    db.session.commit()

    # Now test deleting it
    response = client.delete(f'/inventory/{new_item.id}')
    assert response.status_code == 200
    assert 'message' in response.json
    assert response.json['message'] == 'Item deleted successfully'

def test_delete_inventory_not_found(client, logged_in_user):
    # Test case for deleting a non-existent inventory item
    response = client.delete('/inventory/99999')  # Use an invalid ID
    assert response.status_code == 404
    assert 'error' in response.json
