# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from oauthlib.oauth2 import WebApplicationClient
import requests
import os

auth_blueprint = Blueprint('auth', __name__)

# OAuth2 client setup
google_client_id = os.getenv("GOOGLE_CLIENT_ID")
google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
google_discovery_url = "https://accounts.google.com/.well-known/openid-configuration"

client = WebApplicationClient(google_client_id)

@auth_blueprint.route('/login')
def login():
    return render_template('login.html')

@auth_blueprint.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.home'))

@auth_blueprint.route('/signup')
def signup():
    return render_template('signup.html')

@auth_blueprint.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, username=username, password_hash=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    flash('Signup successful! Welcome, {}'.format(username))
    return redirect(url_for('main.home'))

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.home'))

@auth_blueprint.route('/login/google')
def login_google():
    google_provider_cfg = requests.get(google_discovery_url).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@auth_blueprint.route('/login/google/callback')
def callback():
    try:
        code = request.args.get("code")
        google_provider_cfg = requests.get(google_discovery_url).json()
        token_endpoint = google_provider_cfg["token_endpoint"]

        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(google_client_id, google_client_secret),
        )

        client.parse_request_body_response(token_response.text)

        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        if userinfo_response.json().get("email_verified"):
            unique_id = userinfo_response.json()["sub"]
            users_email = userinfo_response.json()["email"]
            picture = userinfo_response.json()["picture"]
            users_name = userinfo_response.json()["given_name"]
        else:
            flash('Email not verified by Google.')
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(email=users_email).first()

        if not user:
            user = User(
                email=users_email, username=users_name,
                password_hash=generate_password_hash(os.urandom(24))
            )
            db.session.add(user)
            db.session.commit()

        login_user(user)
        flash('Logged in successfully! Welcome, {}'.format(users_name))
        return redirect(url_for('main.home'))

    except Exception as e:
        flash('Login failed due to an error. Please try again.')
        return redirect(url_for('auth.login'))
