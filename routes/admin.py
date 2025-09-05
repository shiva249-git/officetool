from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models import User
from forms.admin_forms import AdminCreateForm, AdminEditUserForm
from werkzeug.security import generate_password_hash

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# ======= Create Admin =======
@admin_bp.route("/create", methods=["GET", "POST"])
def create_admin():
    form = AdminCreateForm()
    if User.query.filter_by(is_admin=True).first():
        flash("Admin already exists!", "warning")
        return redirect(url_for("auth.login"))

    if form.validate_on_submit():
        admin_user = User(
            username=form.username.data,
            email=form.email.data,
            is_admin=True,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(admin_user)
        db.session.commit()
        flash("Admin created successfully! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("admin/create_admin.html", form=form)


# ======= Admin Dashboard - View Users =======
@admin_bp.route("/panel")
@login_required
def panel():
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for("dashboard.index"))

    users = User.query.order_by(User.id.desc()).all()
    return render_template("admin/panel.html", users=users)


# ======= Edit User =======
@admin_bp.route("/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for("dashboard.index"))

    user = User.query.get_or_404(user_id)
    form = AdminEditUserForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data
        if form.password.data:
            user.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash("User updated successfully!", "success")
        return redirect(url_for("admin.panel"))

    return render_template("admin/edit_user.html", form=form, user=user)


# ======= Delete User =======
@admin_bp.route("/delete/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for("dashboard.index"))

    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash("Cannot delete admin user!", "danger")
        return redirect(url_for("admin.panel"))

    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully!", "success")
    return redirect(url_for("admin.panel"))


