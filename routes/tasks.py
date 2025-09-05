from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Task, db, User
from forms.user_forms import TaskForm
from datetime import date

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# ===== List & Create Tasks =====
@tasks_bp.route("/", methods=["GET", "POST"])
@login_required
def tasks_page():
    form = TaskForm()
    # Populate assigned_to choices dynamically
    form.assigned_to.choices = [(u.id, u.username) for u in User.query.all()]

    # Handle task creation
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            status=form.status.data,
            due_date=form.due_date.data,
            user_id=form.assigned_to.data,
            assigned_to=User.query.get(form.assigned_to.data).username
        )
        db.session.add(task)
        db.session.commit()
        flash("Task created successfully!", "success")
        return redirect(url_for("tasks.tasks_page"))

    # Filters & search
    search_query = request.args.get("q", "")
    status_filter = request.args.get("status", "")
    priority_filter = request.args.get("priority", "")

    tasks_query = Task.query
    if not current_user.is_admin:
        tasks_query = tasks_query.filter(Task.user_id == current_user.id)
    if search_query:
        tasks_query = tasks_query.filter(Task.title.ilike(f"%{search_query}%"))
    if status_filter:
        tasks_query = tasks_query.filter_by(status=status_filter)
    if priority_filter:
        tasks_query = tasks_query.filter_by(priority=priority_filter)

    tasks = tasks_query.order_by(Task.due_date.asc()).all()
    today = date.today()

    return render_template(
        "tasks.html",
        tasks=tasks,
        form=form,
        today=today,
        search_query=search_query,
        status_filter=status_filter,
        priority_filter=priority_filter,
        current_user=current_user
    )


# ===== Edit Task =====
@tasks_bp.route("/edit/<int:task_id>", methods=["GET","POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    form.assigned_to.choices = [(u.id, u.username) for u in User.query.all()]

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data
        task.status = form.status.data
        task.due_date = form.due_date.data
        task.user_id = form.assigned_to.data
        task.assigned_to = User.query.get(form.assigned_to.data).username
        db.session.commit()
        flash("Task updated!", "success")
        return redirect(url_for("tasks.tasks_page"))

    form.assigned_to.data = task.user_id
    return render_template("task_form.html", form=form, action="Edit")


# ===== Delete Task =====
@tasks_bp.route("/delete/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted!", "success")
    return redirect(url_for("tasks.tasks_page"))


# ===== Complete Task =====
@tasks_bp.route("/complete/<int:task_id>", methods=["POST"])
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = "Completed"
    db.session.commit()
    flash("Task marked as completed!", "success")
    return redirect(url_for("tasks.tasks_page"))
