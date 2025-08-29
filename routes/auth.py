from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import User, db
from forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# ======= Register =======
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registered successfully! Login now.", "success")
        return redirect(url_for('auth.login'))
    return render_template("register.html", form=form)

# ======= Login =======
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Welcome back!", "success")
            return redirect(url_for('dashboard.home'))  # ✅ after login
        flash("Invalid credentials", "danger")
    return render_template("login.html", form=form)

# ======= Logout =======
@auth_bp.route('/logout')
@login_required   # ✅ protect logout
def logout():
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for('auth.login'))
