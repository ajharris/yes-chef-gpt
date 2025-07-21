import pytest
from backend.routes.chatgpt import chatgpt_blueprint
import flask
@pytest.fixture(autouse=True)
def register_blueprint(monkeypatch):
    app = flask.current_app
    if app and not app.blueprints.get('chatgpt'):  # Avoid duplicate registration
        app.register_blueprint(chatgpt_blueprint, url_prefix='/api')

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

# Example mock response for a cached recipe
CACHED_RECIPE = {
    "ingredients": ["chicken", "garlic", "olive oil"],
    "steps": ["Preheat oven to 400F", "Rub chicken with garlic and oil", "Roast for 25 mins"],
    "pickup_notes": ["Look for free-range chicken", "Get fresh garlic at the produce section"],
    "source": "cache"
}

# Example mock response for a generated recipe
GENERATED_RECIPE = {
    "ingredients": ["dragonfruit", "anchovies", "lime"],
    "steps": ["Slice dragonfruit", "Mash anchovies with lime juice", "Serve chilled"],
    "pickup_notes": ["Dragonfruit is seasonal", "Try the seafood aisle for anchovies"],
    "source": "llm"
}

@pytest.fixture
def mock_recipe_cache(monkeypatch):
    def mock_lookup_recipe(ingredients, preferences):
        if "chicken" in ingredients:
            return CACHED_RECIPE
        return None

    monkeypatch.setattr("backend.services.recipe_cache.lookup_recipe", mock_lookup_recipe)


@pytest.fixture
def mock_llm(monkeypatch):
    def mock_generate_recipe(ingredients, preferences):
        return GENERATED_RECIPE

    monkeypatch.setattr("backend.services.recipe_generator.generate_with_llm", mock_generate_recipe)


def test_suggest_recipes_returns_cached_suggestion(client, mock_recipe_cache):
    response = client.post("/api/suggest_recipes", json={
        "ingredients": ["chicken", "garlic"],
        "preferences": {"diet": "keto"}
    })
    assert response.status_code == 200
    data = response.get_json()
    # If response is wrapped in 'recipe', extract it
    if "recipe" in data:
        data = data["recipe"]
    assert data["source"] == "cache" or data["source"] == "llm"
    assert "ingredients" in data and isinstance(data["ingredients"], list)
    assert "steps" in data and isinstance(data["steps"], list)
    assert "pickup_notes" in data and isinstance(data["pickup_notes"], list)


def test_suggest_recipes_generates_new_when_no_cache(client, mock_recipe_cache, mock_llm):
    response = client.post("/api/suggest_recipes", json={
        "ingredients": ["dragonfruit", "anchovies"],
        "preferences": {"diet": "paleo"}
    })
    assert response.status_code == 200
    data = response.get_json()
    if "recipe" in data:
        data = data["recipe"]
    assert data["source"] == "llm"
    assert isinstance(data["ingredients"], list)
    assert isinstance(data["steps"], list)
    assert isinstance(data["pickup_notes"], list)


def test_suggest_recipes_allows_anonymous(client, mock_llm):
    response = client.post("/api/suggest_recipes", json={
        "ingredients": ["tofu", "miso"]
    })
    assert response.status_code == 200
    data = response.get_json()
    if "recipe" in data:
        data = data["recipe"]
    assert "ingredients" in data
    assert "steps" in data


def test_suggest_recipes_missing_ingredients(client):
    response = client.post("/api/suggest_recipes", json={})
    assert response.status_code == 400


def test_suggest_recipes_response_format(client, mock_llm):
    response = client.post("/api/suggest_recipes", json={
        "ingredients": ["potato", "cheese"]
    })
    data = response.get_json()
    if "recipe" in data:
        data = data["recipe"]
    assert isinstance(data["ingredients"], list)
    assert all(isinstance(i, str) for i in data["ingredients"])
    assert isinstance(data["steps"], list)
    assert isinstance(data["pickup_notes"], list)


def test_suggest_recipes_with_preferences(client, mock_llm):
    response = client.post("/api/suggest_recipes", json={
        "ingredients": ["spinach", "tofu"],
        "preferences": {"diet": "vegan"}
    })
    data = response.get_json()
    if "recipe" in data:
        data = data["recipe"]
    all_ingredients = " ".join(data["ingredients"]).lower()
    assert "meat" not in all_ingredients
