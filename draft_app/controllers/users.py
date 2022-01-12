from flask import app
from flask import render_template, request, redirect, session, flash
from werkzeug.utils import redirect
from draft_app import app
from draft_app.models.user import User
from draft_app.models.player import Player
from draft_app.controllers import general
from flask_bcrypt import Bcrypt
import json
import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# --> Display Routes <--

# index
@app.route("/")
def home():
    # redirect if admin logged in
    if "is_admin" in session:
        return redirect("/dev_controls")
    # redirect if user logged in
    elif "user_id" in session:
        return redirect("users/dashboard")
    else:
        return render_template("index.html")

# dashboard
@app.route("/users/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session['user_id']
    }
    user = User.get_user_by_id(data)
    return render_template("dashboard.html", user = user)

# recommendations
@app.route("/users/recommendations")
def recommendations():
    if "user_id" not in session:
        return redirect("/guest/recommendations")
    data = {
        "id": session['user_id']
    }
    user = User.get_user_by_id(data)
    return render_template("loggedin.html", user = user)

# guest
@app.route("/guest/recommendations")
def guest():
    return render_template("guest.html")

# advanced
@app.route("/users/recommendations/advanced")
def users_advanced():
    player_names = general.get_player_names()
    return render_template("advanced.html", player_names = json.dumps(player_names))

@app.route("/guest/recommendations/advanced")
def guest_advanced():
    player_names = general.get_player_names()
    return render_template("advanced.html", player_names = json.dumps(player_names))

# settings
@app.route("/users/account")
def user_account():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session['user_id']
    }
    user = User.get_user_by_id(data)
    return render_template("user_settings.html", user = user)


# --> Action Routes <--

# register
@app.route("/users/register", methods=['POST'])
def register_user():
    check = User.validate_user(request.form)
    if not check:
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password_input'])
    data = {
        "user_name": request.form['user_name_input'],
        "email":request.form['email_input'],
        "password": pw_hash
    }
    user = User.new_user(data)
    print(user)
    session['user_id'] = user
    return redirect("/users/dashboard")

# login
@app.route("/users/login", methods=['POST'])
def login_user():
    data = {
            "email": request.form['email_login'],
            "password": request.form['password_login']
        }
    # confirm user credentials
    if not User.validate_login(data):
        return redirect("/")
    else:
        user = User.get_user_by_email(data)
        session['user_id'] = user.id
        return redirect("/users/dashboard")

# logout
@app.route("/users/logout")
def logout_user():
    session.clear()
    return redirect("/")