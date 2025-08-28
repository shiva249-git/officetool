from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

# In-memory user storage for demo
users_db = {}

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = users_db.get(email)
        if user and check_password_hash(user['password_hash'], password):
            session['user_email'] = email
            return redirect(url_for("dashboard.home"))
        flash("Invalid credentials", "danger")
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        if email in users_db:
            flash("User already exists", "danger")
        else:
            users_db[email] = {"name": name, "password_hash": generate_password_hash(password)}
            flash("Registration successful. Please login.", "success")
            return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user_email", None)
    return redirect(url_for("auth.login"))
