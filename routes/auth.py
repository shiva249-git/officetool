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
        if User.query.filter_by(email=form.email.data).first():
            flash("User already exists!", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            username=form.username.data,
            email=form.email.data,
            is_admin=False
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!", "success")
        login_user(user)
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
