from flask_login import UserMixin, login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from datetime import datetime, timedelta

from backend import db, bcrypt

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    inventory = db.relationship('Inventory', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
            self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    fiber_content = db.Column(db.Float, nullable=True)  # in grams
    sugar_content = db.Column(db.Float, nullable=True)  # in grams
    nutrition_score = db.Column(db.Float, nullable=True)  # overall nutrition score
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref=db.backref('recipes', lazy=True))
    ratings = db.relationship('Rating', backref='recipe', lazy=True)

    def __repr__(self):
        return f'<Recipe {self.title}>'

def average_rating(self):
    if not self.ratings or len(self.ratings) == 0:
        return None
    return sum(rating.score for rating in self.ratings) / len(self.ratings)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    def __repr__(self):
        return f'<Rating {self.score} for Recipe ID {self.recipe_id}>'

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ingredient = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=True)  # Allow null values
    unit = db.Column(db.String(20), nullable=True)  # Allow null values

    def serialize(self):
        return {
            'id': self.id,
            'ingredient': self.ingredient,
            'quantity': self.quantity,  # Could be null
            'unit': self.unit  # Could be null
        }

    
class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    spot_name = db.Column(db.String(128), nullable=False)  # Name of the spot (e.g., 'stove', 'sink', etc.)
    last_cleaned = db.Column(db.DateTime, default=datetime.utcnow)
    next_reminder = db.Column(db.DateTime)
    reminder_interval_days = db.Column(db.Integer, default=30)  # Default reminder interval (30 days)
    user = db.relationship('User', backref=db.backref('reminders', lazy=True))

    def __init__(self, user_id, spot_name, reminder_interval_days=30):
        self.user_id = user_id
        self.spot_name = spot_name
        self.reminder_interval_days = reminder_interval_days
        self.last_cleaned = datetime.utcnow()
        self.next_reminder = self.last_cleaned + timedelta(days=self.reminder_interval_days)

    def update_last_cleaned(self):
        """
        Updates the last cleaned date to now and recalculates the next reminder.
        """
        self.last_cleaned = datetime.utcnow()
        self.next_reminder = self.last_cleaned + timedelta(days=self.reminder_interval_days)
        db.session.commit()

    def set_reminder_interval(self, days):
        """
        Allows the user to customize the reminder interval.
        """
        self.reminder_interval_days = days
        self.next_reminder = self.last_cleaned + timedelta(days=days)
        db.session.commit()

    @staticmethod
    def get_active_reminders(user_id):
        """
        Retrieves all reminders that are due (next_reminder is in the past or now).
        """
        now = datetime.utcnow()
        return Reminder.query.filter_by(user_id=user_id, is_active=True).all()

login_manager.session_protection = "strong"
