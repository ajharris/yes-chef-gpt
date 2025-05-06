import pytest
from flask import Flask
from backend.models import Recipe, User
from backend.extensions import db

@pytest.fixture
def mock_current_user(mocker):
    mock_user = mocker.patch('flask_login.utils._get_user')
    mock_user.return_value = User(username='testuser', email='test@example.com', dietary_preferences=['vegan'])
    return mock_user

@pytest.mark.usefixtures("mock_current_user")
def test_returns_valid_recipe(client, mocker):
    # Mock database query
    mock_recipe = Recipe(
        ingredients="Tomato, Cheese",
        preparation="Mix and cook",
        pickup="Serve hot",
        raw_ingredients=["Tomato", "Cheese"]
    )
    mocker.patch('backend.models.Recipe.query.filter_by', return_value=mocker.Mock(first=lambda: mock_recipe))

    response = client.post('/api/suggest_recipes', json={"ingredients": ["Tomato", "Cheese"]})  # Correct URL

    assert response.status_code == 200
    assert response.json == {
        "recipe": {
            "ingredients": "Tomato, Cheese",
            "preparation": "Mix and cook",
            "pickup": "Serve hot"
        }
    }

def test_rejects_missing_ingredients(client):
    response = client.post('/api/suggest_recipes', json={})
    assert response.status_code == 400
    assert response.json == {"error": "Missing ingredients field"}

def test_rejects_invalid_ingredients_format(client):
    response = client.post('/api/suggest_recipes', json={"ingredients": "Not a list"})
    assert response.status_code == 422
    assert response.json == {"error": "Ingredients must be a list of strings"}

def test_handles_chatgpt_failure(client, mocker):
    # Mock ChatGPT API failure
    mocker.patch('openai.ChatCompletion.create', side_effect=Exception("API Error"))

    response = client.post('/api/suggest_recipes', json={"ingredients": ["Tomato", "Cheese"]})

    assert response.status_code == 500
    assert "Failed to generate recipes" in response.json["error"]

def test_user_preferences_get(client, mocker):
    # Mock current_user with dietary preferences
    mock_user = mocker.patch('flask_login.utils._get_user')
    mock_user.return_value.dietary_preferences = ["vegan", "gluten-free"]

    response = client.get('/auth/api/user/preferences')  # Updated URL

    assert response.status_code == 200
    assert response.json == {"dietary_preferences": ["vegan", "gluten-free"]}

def test_user_preferences_update(client, mocker):
    # Mock current_user
    mock_user = mocker.patch('flask_login.utils._get_user')
    mock_user.return_value.dietary_preferences = []

    response = client.post('/auth/api/user/preferences', json={"dietary_preferences": ["keto", "halal"]})  # Updated URL

    assert response.status_code == 200
    assert response.json == {"message": "Dietary preferences updated successfully"}
    assert mock_user.return_value.dietary_preferences == ["keto", "halal"]

def test_suggest_recipes_with_stored_preferences(client, mocker):
    # Mock current_user with dietary preferences
    mock_user = mocker.patch('flask_login.utils._get_user')
    mock_user.return_value.dietary_preferences = ["vegan"]

    # Mock ChatGPT API response
    mock_chatgpt = mocker.patch('openai.ChatCompletion.create')
    mock_chatgpt.return_value = {
        'choices': [{
            'message': {
                'content': "Ingredients: Tomato, Lettuce\nPreparation: Mix\nPickup: Serve"
            }
        }]
    }

    response = client.post('/api/suggest_recipes', json={"ingredients": ["Tomato", "Lettuce"]})

    assert response.status_code == 200
    assert "vegan" in mock_chatgpt.call_args[1]['messages'][1]['content']

def test_suggest_recipes_override_preferences(client, mocker):
    # Mock current_user with dietary preferences
    mock_user = mocker.patch('flask_login.utils._get_user')
    mock_user.return_value.dietary_preferences = ["vegan"]

    # Mock ChatGPT API response
    mock_chatgpt = mocker.patch('openai.ChatCompletion.create')
    mock_chatgpt.return_value = {
        'choices': [{
            'message': {
                'content': "Ingredients: Chicken, Rice\nPreparation: Cook\nPickup: Serve"
            }
        }]
    }

    response = client.post('/api/suggest_recipes', json={"ingredients": ["Chicken", "Rice"], "dietary_restrictions": ["keto"]})

    assert response.status_code == 200
    assert "keto" in mock_chatgpt.call_args[1]['messages'][1]['content']
    assert "vegan" not in mock_chatgpt.call_args[1]['messages'][1]['content']

def test_suggest_recipes_with_dietary_labels(client, mocker):
    # Mock current_user with dietary preferences
    mock_user = mocker.patch('flask_login.utils._get_user')
    mock_user.return_value.dietary_preferences = ["vegan"]

    # Mock ChatGPT API response
    mock_chatgpt = mocker.patch('openai.ChatCompletion.create')
    mock_chatgpt.return_value = {
        'choices': [{
            'message': {
                'content': "Ingredients: Tomato, Lettuce\nPreparation: Mix\nPickup: Serve\nDietary Label: Vegan"
            }
        }]
    }

    response = client.post('/api/suggest_recipes', json={"ingredients": ["Tomato", "Lettuce"]})

    assert response.status_code == 200
    assert "Dietary Label: Vegan" in response.json["recipe"]["pickup"]