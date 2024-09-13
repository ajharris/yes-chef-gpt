import pytest
from backend import create_app, db
from backend.models import User  # Import your models as needed
from backend.extensions import db, bcrypt

@pytest.fixture
def app():
    # Pass the test configuration
    app = create_app('backend.test_config.TestConfig')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def init_database():
    # Create the database and the tables
    db.create_all()

    # Add a sample user for testing purposes
    user = User(email="test@example.com", username="testuser")
    user.set_password("testpassword")  # Use the setter to hash the password
    db.session.add(user)
    db.session.commit()

    yield db  # Allow tests to use the database

    db.drop_all()  # Clean up after the tests
