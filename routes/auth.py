from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, csrf
from models import User
from forms.user_forms import LoginForm, RegisterForm

auth_bp = Blueprint("auth", __name__)

# ===== Create Admin (one-time) =====
@auth_bp.route("/create-admin", methods=["GET", "POST"])
def create_admin():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_admin = User.query.filter_by(is_admin=True).first()
        if existing_admin:
            flash("Admin already exists!", "danger")
            return redirect(url_for("auth.login"))

        admin = User(username=username, email=email, is_admin=True)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()

        flash("Admin account created! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("create_admin.html")

# ===== User Registration =====
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print("DEBUG: form.username.data =", form.username.data)
        print("DEBUG: form.email.data =", form.email.data)
        print("DEBUG: form.password.data =", form.password.data)
        print("DEBUG: form.errors =", form.errors)

        # Check if user already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("User already exists!", "danger")
            print("DEBUG: User already exists:", form.email.data)
            return redirect(url_for("auth.register"))

        # Create user object
        user = User(
            username=form.username.data,
            email=form.email.data,
            is_admin=False
        )

        # Set password
        try:
            user.set_password(form.password.data)
        except Exception as e:
            print("❌ Password hash error:", e)
            flash("Error setting password", "danger")
            return redirect(url_for("auth.register"))

        # Add to session
        db.session.add(user)
        try:
            db.session.commit()
            print("✅ User committed:", user.id, user.email)
        except Exception as e:
            db.session.rollback()
            print("❌ Commit failed:", e)
            flash("Database error: could not create user", "danger")
            return redirect(url_for("auth.register"))

        # Log in the user
        try:
            login_user(user)
            print("✅ User logged in:", user.id)
        except Exception as e:
            print("❌ Login failed:", e)
            flash("Error logging in", "danger")
            return redirect(url_for("auth.register"))

        flash("Account created successfully!", "success")
        return redirect(url_for("dashboard.home"))

    return render_template("auth/register.html", form=form)

# ===== User Login =====
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.user_identifier.data
        # Allow login via username or email
        user = User.query.filter(
            (User.email == identifier) | (User.username == identifier)
        ).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully!", "success")
            next_page = request.args.get("next")
            if user.is_admin:
                return redirect(next_page or url_for("admin.admin_dashboard"))
            return redirect(next_page or url_for("dashboard.home"))
        else:
            flash("Invalid username/email or password", "danger")
    return render_template("auth/login.html", form=form)

# ===== Logout =====
@auth_bp.route("/logout", methods=["POST"])
@login_required
@csrf.exempt  # only if CSRF is global
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
