# config.py

import os

def fix_postgres_dialect(url):
    if url and url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url

DATABASE_URL = fix_postgres_dialect(os.getenv("DATABASE_URL"))

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set or is invalid")

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OAuth credentials
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    FACEBOOK_CLIENT_ID = os.environ.get('FACEBOOK_CLIENT_ID')
    FACEBOOK_CLIENT_SECRET = os.environ.get('FACEBOOK_CLIENT_SECRET')
    
    # OAuth redirect URIs
    GOOGLE_REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI')
    FACEBOOK_REDIRECT_URI = os.environ.get('FACEBOOK_REDIRECT_URI')

# Test the database connection
import psycopg2
from psycopg2 import OperationalError

def test_db_connection():
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                print("Database connection successful:", cursor.fetchone())
                print("SQLALCHEMY_DATABASE_URI:", DATABASE_URL)
    except OperationalError as e:
        print("Database connection failed:", e)


# test_db_connection()