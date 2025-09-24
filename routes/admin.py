# routes/admin.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import User, Task, Billing, db
from forms.user_forms import UserEditForm

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# ===== Admin Dashboard =====
@admin_bp.route("/dashboard")
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for("dashboard.home"))

    total_users = User.query.count()
    total_admins = User.query.filter_by(is_admin=True).count()
    total_tasks = Task.query.count()
    pending_tasks = Task.query.filter_by(status="Pending").count()
    completed_tasks = Task.query.filter_by(status="Completed").count()
    total_bills = Billing.query.count() if 'Billing' in globals() else 0  # if Billing model exists

    return render_template(
        "admin/admin_dashboard.html",
        total_users=total_users,
        total_admins=total_admins,
        total_tasks=total_tasks,
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        total_bills=total_bills
    )

# ===== Admin Panel: Users List =====
@admin_bp.route("/panel")
@login_required
def panel():
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for("dashboard.home"))

    users = User.query.all()
    return render_template("admin/panel.html", users=users)

# ===== Edit User =====
@admin_bp.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for("dashboard.home"))

    user = User.query.get_or_404(user_id)
    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data
        db.session.commit()
        flash("User updated successfully!", "success")
        return redirect(url_for("admin.panel"))

    return render_template("admin/edit_user.html", form=form, user=user)

# ===== Delete User =====
@admin_bp.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for("dashboard.home"))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully!", "success")
    return redirect(url_for("admin.panel"))

# ===== Billing Overview =====
@admin_bp.route("/billing")
@login_required
def billing():
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for("dashboard.home"))

    bills = Billing.query.all() if 'Billing' in globals() else []
    return render_template("admin/billing.html", bills=bills)
