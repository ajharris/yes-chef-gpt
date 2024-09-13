from flask import Blueprint, request, jsonify
from flask_login import current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required
from backend.models import Reminder, User
from backend import db

auth_blueprint = Blueprint('auth', __name__)

# Login route
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    login_user(user)
    return jsonify({'message': 'Login successful'}), 200


# Signup route

@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not email:
            return jsonify({'error': 'Email is required'}), 400
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        if not password:
            return jsonify({'error': 'Password is required'}), 400

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'User already exists'}), 400

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Signup successful'}), 201
    except Exception as e:
        print(f"Error during signup: {e}")  # Log the actual error in the terminal
        return jsonify({'error': 'Internal Server Error'}), 500
                         

# Logout route
@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_blueprint.route('/reminder', methods=['POST'])
@login_required
def add_reminder():
    data = request.json
    spot_name = data.get('spot_name')
    reminder_interval_days = data.get('reminder_interval_days', 30)  # Optional, default to 30 days

    new_reminder = Reminder(user_id=current_user.id, spot_name=spot_name, reminder_interval_days=reminder_interval_days)
    
    db.session.add(new_reminder)
    db.session.commit()

    return jsonify({'message': f'Reminder for {spot_name} created successfully'}), 201

@auth_blueprint.route('/reminders/active', methods=['GET'])
@login_required
def get_active_reminders():
    reminders = Reminder.get_active_reminders(current_user.id)
    reminder_list = [{
        'spot_name': reminder.spot_name,
        'next_reminder': reminder.next_reminder,
        'last_cleaned': reminder.last_cleaned
    } for reminder in reminders]

    return jsonify(reminder_list), 200

@auth_blueprint.route('/reminder/<int:reminder_id>/update', methods=['PUT'])
@login_required
def update_reminder(reminder_id):
    reminder = Reminder.query.get_or_404(reminder_id)
    
    if reminder.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403

    reminder.update_last_cleaned()
    
    return jsonify({'message': f'{reminder.spot_name} reminder updated successfully'}), 200
