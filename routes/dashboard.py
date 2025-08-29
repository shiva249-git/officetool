from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Task, db
from forms import TaskForm

# No url_prefix → dashboard will be at "/"
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def home():
    # Fetch all tasks for the logged-in user
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    form = TaskForm()
    return render_template("dashboard.html", user_email=current_user.email, tasks=tasks, form=form)


@dashboard_bp.route('/tasks/create', methods=['POST'])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(
            title=form.title.data,
            priority=form.priority.data,
            status='Pending',
            due_date=form.due_date.data,
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        flash("Task created successfully!", "success")
    else:
        flash("Failed to create task. Check the input fields.", "danger")

    return redirect(url_for('dashboard.home'))
