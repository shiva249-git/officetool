from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from models import Task, User
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks")
def list_tasks():
    if "user_email" not in session:
        return redirect(url_for("auth.login"))
    user = User.query.filter_by(email=session["user_email"]).first()
    tasks = Task.query.all()  # Show all tasks
    return render_template("tasks.html", tasks=tasks, user=user)

@tasks_bp.route("/tasks/add", methods=["POST"])
def add_task():
    if "user_email" not in session:
        return redirect(url_for("auth.login"))

    title = request.form.get("title")
    description = request.form.get("description")
    assigned_to_email = request.form.get("assigned_to")
    due_date = request.form.get("due_date")
    priority = request.form.get("priority", "Medium")

    assigned_user = User.query.filter_by(email=assigned_to_email).first()
    if not assigned_user:
        flash("Assigned user not found", "danger")
        return redirect(url_for("tasks.list_tasks"))

    task = Task(
        title=title,
        description=description,
        assigned_to=assigned_user.id,
        priority=priority,
        due_date=datetime.strptime(due_date, "%Y-%m-%d") if due_date else None
    )
    db.session.add(task)
    db.session.commit()
    flash("Task added successfully", "success")
    return redirect(url_for("tasks.list_tasks"))
