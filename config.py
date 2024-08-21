import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///chefgpt.db').replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
