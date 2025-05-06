import pytest
from backend import create_app
from backend.models import db, User

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def init_database(app):
    with app.app_context():
        db.drop_all()  # Ensure a clean state
        db.create_all()  # Create all tables
        db.session.commit()
        # Seed the database with a test user
        test_user = User(username='testuser', email='test@example.com')
        test_user.set_password('testpassword')
        db.session.add(test_user)
        db.session.commit()
        yield
        db.session.remove()
        db.drop_all()


# ---- Test Auth Routes ----

def test_signup(client):
    response = client.post('/auth/signup', json={  # Use the correct URL prefix
        'email': 'newuser@example.com',
        'username': 'newuser',
        'password': 'testpassword'
    })
    assert response.status_code == 201


def test_login(client, init_database, mocker):
    # Mocking user login
    mocker.patch('backend.models.User.check_password', return_value=True)
    
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    
    assert response.status_code == 200
    assert b"Logged in successfully" in response.data


def test_logout(client, init_database):
    # First log in
    client.post('/auth/login', json={  # Use the /auth prefix
        'email': 'test@example.com',
        'password': 'testpassword'
    })

    # Then log out
    response = client.post('/auth/logout')  # Use the /auth prefix
    assert response.status_code == 200



