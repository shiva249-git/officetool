from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models import Task, User
from forms.user_forms import TaskForm
from datetime import date
from sqlalchemy import or_

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

# --- Dashboard Home ---
@dashboard_bp.route("/", methods=["GET"])
@login_required
def home():
    if current_user.is_admin:
        tasks_query = Task.query
    else:
        tasks_query = Task.query.filter(
    (Task.assigned_to == current_user.id) | (Task.user_id == current_user.id)
)
    # Filters
    status_filter = request.args.get("status")
    priority_filter = request.args.get("priority")
    search_query = request.args.get("q")

    if status_filter:
        tasks_query = tasks_query.filter_by(status=status_filter)
    if priority_filter:
        tasks_query = tasks_query.filter_by(priority=priority_filter)
    if search_query:
        tasks_query = tasks_query.filter(
            or_(Task.title.ilike(f"%{search_query}%"),
                Task.description.ilike(f"%{search_query}%"))
        )

    tasks = tasks_query.all()

    # Form
    form = TaskForm()
    form.assigned_to.choices = [(u.id, u.username) for u in User.query.all()]

    # Task summaries
    total_tasks = len(tasks)
    pending_tasks = len([t for t in tasks if t.status == "Pending"])
    completed_tasks = len([t for t in tasks if t.status == "Completed"])
    overdue_tasks = len([t for t in tasks if t.due_date and t.due_date < date.today() and t.status != "Completed"])

    return render_template(
        "dashboard.html",
        tasks=tasks,
        form=form,
        total_tasks=total_tasks,
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        overdue_tasks=overdue_tasks,
        status_filter=status_filter,
        priority_filter=priority_filter,
        search_query=search_query,
        today=date.today()
    )


# --- Create Task ---
@dashboard_bp.route("/create_task", methods=["POST"])
@login_required
def create_task():
    form = TaskForm()
    form.assigned_to.choices = [(u.id, u.username) for u in User.query.all()]

    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            user_id=current_user.id,
            assigned_to=form.assigned_to.data,
            priority=form.priority.data,
            status=form.status.data,
            due_date=form.due_date.data
        )
        db.session.add(task)
        db.session.commit()
        flash("Task created successfully!", "success")
    else:
        flash("Error creating task.", "danger")

    return redirect(url_for("dashboard.home"))


# --- Edit Task ---
@dashboard_bp.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if not current_user.is_admin and task.assigned_to != current_user.id:
        flash("Not authorized!", "danger")
        return redirect(url_for("dashboard.home"))

    form = TaskForm(obj=task)
    form.assigned_to.choices = [(u.id, u.username) for u in User.query.all()]

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.assigned_to = form.assigned_to.data
        task.priority = form.priority.data
        task.status = form.status.data
        task.due_date = form.due_date.data
        db.session.commit()
        flash("Task updated successfully!", "success")
        return redirect(url_for("dashboard.home"))

    return render_template("edit_task.html", form=form, task=task)


# --- Delete Task ---
@dashboard_bp.route("/delete_task/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    if not current_user.is_admin and task.assigned_to != current_user.id:
        task.deletion_requested = True
        db.session.commit()
        flash("Deletion request sent to admin!", "info")
    else:
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted!", "success")

    return redirect(url_for("dashboard.home"))


# --- Complete Task ---
@dashboard_bp.route("/complete_task/<int:task_id>")
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if not current_user.is_admin and task.assigned_to != current_user.id:
        flash("Not authorized!", "danger")
        return redirect(url_for("dashboard.home"))

    task.status = "Completed"
    db.session.commit()
    flash("Task marked as completed!", "success")
    return redirect(url_for("dashboard.home"))


@dashboard_bp.route("/tasks")
@login_required
def tasks_page():
    # Base query
    tasks_query = Task.query if current_user.is_admin else Task.query.filter_by(assigned_to=current_user.id)

    # Filters
    status_filter = request.args.get("status")
    priority_filter = request.args.get("priority")
    search_query = request.args.get("q")

    if status_filter:
        tasks_query = tasks_query.filter_by(status=status_filter)
    if priority_filter:
        tasks_query = tasks_query.filter_by(priority=priority_filter)
    if search_query:
        tasks_query = tasks_query.filter(
            or_(
                Task.title.ilike(f"%{search_query}%"),
                Task.description.ilike(f"%{search_query}%")
            )
        )

    tasks = tasks_query.all()
    today = date.today()
    return render_template("tasks.html", tasks=tasks, status_filter=status_filter,
                           priority_filter=priority_filter, search_query=search_query, today=today)


# --- Billing / Invoice ---
@dashboard_bp.route("/billing")
@login_required
def billing():
    if not current_user.is_admin:
        return "Access denied", 403

    completed_tasks = Task.query.filter_by(status="Completed").all()
    return render_template("billing.html", tasks=completed_tasks)


# --- Generate Invoice ---
@dashboard_bp.route("/generate_invoice/<int:task_id>")
@login_required
def generate_invoice(task_id):
    if not current_user.is_admin:
        return "Access denied", 403

    task = Task.query.get_or_404(task_id)
    return render_template("invoice.html", task=task)
