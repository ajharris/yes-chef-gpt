import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_login import LoginManager, UserMixin
from backend.routes.chatgpt import chatgpt_blueprint
from backend.tests.conftest import mock_current_user

class MockUser(UserMixin):
    def __init__(self, id):
        self.id = id

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(chatgpt_blueprint, url_prefix='/api')

    # Mock login manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return MockUser(user_id)

    app.config['LOGIN_DISABLED'] = True  # Disable login for testing
    return app
@pytest.fixture(autouse=True)
def mock_openai(monkeypatch):
    import json
    class DummyChatCompletion:
        @staticmethod
        def create(*args, **kwargs):
            # If ingredients is empty, return a list of recipes
            ingredients = kwargs.get('messages', [{}])[0].get('content', '')
            if '[]' in str(ingredients):
                recipes = [
                    {
                        "ingredients": ["mock_ingredient1", "mock_ingredient2"],
                        "steps": ["mock_step1", "mock_step2"],
                        "pickup_notes": ["mock_note1", "mock_note2"],
                        "source": "llm"
                    }
                ]
                return {'choices': [{'message': {'content': json.dumps({"recipes": recipes})}}]}
            recipe = {
                "ingredients": ["mock_ingredient1", "mock_ingredient2"],
                "steps": ["mock_step1", "mock_step2"],
                "pickup_notes": ["mock_note1", "mock_note2"],
                "source": "llm"
            }
            return {'choices': [{'message': {'content': json.dumps(recipe)}}]}
    monkeypatch.setattr('backend.routes.chatgpt.openai', type('MockOpenAI', (), {'ChatCompletion': DummyChatCompletion}))

@pytest.fixture(autouse=True)
def init_db(app):
    from backend.extensions import db
    with app.app_context():
        db.init_app(app)
        db.create_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.mark.usefixtures("mock_current_user")
def test_suggest_recipes_valid_request(client: FlaskClient):
    response = client.post('/api/suggest_recipes', json={
        'ingredients': ['chicken', 'rice'],
        'dietary_restrictions': ['gluten-free']
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'recipe' in data
    assert isinstance(data['recipe'], dict)

def test_suggest_recipes_missing_ingredients(client: FlaskClient):
    response = client.post('/api/suggest_recipes', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Missing ingredients field'

def test_suggest_recipes_invalid_ingredients_format(client: FlaskClient):
    response = client.post('/api/suggest_recipes', json={
        'ingredients': 'not-a-list'
    })
    assert response.status_code == 422
    data = response.get_json()
    assert data['error'] == 'Ingredients must be a list of strings'

def test_suggest_recipes_empty_ingredients(client: FlaskClient):
    response = client.post('/api/suggest_recipes', json={
        'ingredients': []
    })
    assert response.status_code == 200
    data = response.get_json()
    # Accept either 'recipes' or 'recipe' in the response
    if 'recipes' in data:
        assert isinstance(data['recipes'], list)
    elif 'recipe' in data:
        assert isinstance(data['recipe'], dict)
    else:
        assert False, "Response must contain 'recipes' or 'recipe' key"

def test_suggest_recipes_server_error(client: FlaskClient, monkeypatch):
    def mock_openai_chat_completion(*args, **kwargs):
        raise Exception("Mocked server error")  # Simulate a server error

    monkeypatch.setattr('backend.routes.chatgpt.openai.ChatCompletion.create', mock_openai_chat_completion)

    response = client.post('/api/suggest_recipes', json={
        'ingredients': ['chicken', 'rice']
    })
    assert response.status_code == 500  # Expecting a server error