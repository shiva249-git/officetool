from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from models import db, Task, User
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

# ------------------------
# Dashboard - List Tasks
# ------------------------
@tasks_bp.route("/dashboard")
@login_required
def dashboard():
    user = User.query.filter_by(email=session['user_email']).first()
    tasks = Task.query.filter_by(user_id=user.id).order_by(Task.due_date.asc()).all()
    return render_template("dashboard.html", user_email=session['user_email'], tasks=tasks)

# ------------------------
# Create Task
# ------------------------
@tasks_bp.route("/tasks/create", methods=["POST"])
@login_required
def create_task():
    title = request.form.get("title")
    priority = request.form.get("priority")
    due_date = request.form.get("due_date")
    
    if not title:
        flash("Task title is required.", "danger")
        return redirect(url_for('tasks.dashboard'))

    user = User.query.filter_by(email=session['user_email']).first()
    new_task = Task(
        title=title,
        status="Pending",
        priority=priority,
        due_date=datetime.strptime(due_date, "%Y-%m-%d") if due_date else None,
        user_id=user.id
    )
    db.session.add(new_task)
    db.session.commit()
    flash("Task created successfully!", "success")
    return redirect(url_for('tasks.dashboard'))

# ------------------------
# Edit Task
# ------------------------
@tasks_bp.route("/tasks/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == "POST":
        task.title = request.form.get("title")
        task.priority = request.form.get("priority")
        task.status = request.form.get("status")
        due_date = request.form.get("due_date")
        task.due_date = datetime.strptime(due_date, "%Y-%m-%d") if due_date else None

        db.session.commit()
        flash("Task updated successfully!", "success")
        return redirect(url_for('tasks.dashboard'))

    return render_template("edit_task.html", task=task)

# ------------------------
# Delete Task
# ------------------------
@tasks_bp.route("/tasks/delete/<int:task_id>")
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!", "success")
    return redirect(url_for('tasks.dashboard'))

