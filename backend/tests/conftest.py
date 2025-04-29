import os
import pytest
from backend.tests.test_auth_routes import app, create_app
from backend.extensions import db  # Import db instance
from backend.models import User, Recipe, Rating, Inventory  # Ensure all models are imported

# Set a mock DATABASE_URL for testing
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def app():
    app = create_app(test_config=True)  # or however you configure your app
    with app.app_context():
        db.create_all()  # Create all tables before tests
        # Add a test user to ensure the table is populated
        test_user = User(username='testuser', email='test@example.com')
        test_user.set_password('testpassword')
        db.session.add(test_user)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()
