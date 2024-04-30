from flask import Blueprint, render_template, request, session, redirect

from hashlib import sha512

from database import db
from structures import *
from utils import redirect_with_error

from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'user' in session or not session['user']['admin']:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

def is_logged_in():
    return 'user' in session

auth = Blueprint("auth", __name__)

@auth.route("/api/login", methods=["POST"])
def login():
    if not "username" in request.form or not "password" in request.form:
        return redirect_with_error("/login", "Missing parameters")
    
    user = db.get_user_by_name(request.form["username"])

    if user is None:
        return redirect_with_error("/login", "User not found")
    
    if user.password != sha512(request.form["password"].encode()).hexdigest():
        return redirect_with_error("/login", "Incorrect password")
    
    session['user'] = user

    return redirect("/")

@auth.route("/api/register", methods=["POST"])
def register():
    if not "username" in request.form or not "password" in request.form or not "email" in request.form:
        return redirect_with_error("/login", "Missing parameters")
    
    if db.get_user_by_name(request.form["username"]) is not None:
        return redirect_with_error("/login", "Username already taken")
    
    if db.get_user_by_email(request.form["email"]) is not None:
        return redirect_with_error("/login", "Email already taken")
    
    if len(request.form["password"]) > 32 or len(request.form["password"]) < 8:
        return redirect_with_error("/login", "Password must be between 8 and 32 characters")

    password_hash = sha512(request.form["password"].encode()).hexdigest()

    user_object = User(
        id = 0, # this gets replaced by the create_user function, as noted in the docstring
        name = request.form["username"],
        password = password_hash,
        email = request.form["email"],
        admin = len(db.get_all_users()) == 0
    )
    
    db.create_user(user_object)

    session['user'] = user_object

    return redirect("/")

@auth.route("/login")
def login_page():
    return render_template("auth/login.html.j2")

@auth.route("/logout")
@login_required
def logout():
    session.pop("user", None)

    return redirect("/")