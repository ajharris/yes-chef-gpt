from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from backend.models import User
from backend.extensions import db, bcrypt

# Define the authentication blueprint
auth_blueprint = Blueprint('auth', __name__)

# Route to handle user signup
@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    # Ensure that the user does not already exist
    if user:
        return jsonify({'error': 'User already exists'}), 400
    
    # Create a new user and hash the password
    new_user = User(email=data['email'], username=data['username'])
    new_user.set_password(data['password'])  # Use the setter to hash the password
    
    # Add and commit the user to the database
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

# Route to handle user login
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    # Check if the user exists and the password is correct
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({"message": "Logged in successfully"})
    
    return jsonify({"error": "Invalid credentials"}), 401

# Route to handle user logout
@auth_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200
