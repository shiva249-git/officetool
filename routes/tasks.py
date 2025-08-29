from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from models import Task, db
from forms import TaskForm

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

# ======= Create Task =======
@tasks_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            assigned_to=form.assigned_to.data,
            priority=form.priority.data,
            status=form.status.data,
            due_date=form.due_date.data
        )
        db.session.add(task)
        db.session.commit()
        flash("Task created successfully!", "success")
        return redirect(url_for('dashboard.home'))
    return render_template("dashboard.html", form=form, user_email=current_user.email, tasks=current_user.tasks)

# ======= Edit Task =======
@tasks_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.assigned_to = form.assigned_to.data
        task.priority = form.priority.data
        task.status = form.status.data
        task.due_date = form.due_date.data
        db.session.commit()
        flash("Task updated successfully!", "success")
        return redirect(url_for('dashboard.home'))
    return render_template("edit_task.html", form=form, task=task)

# ======= Delete Task =======
@tasks_bp.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully!", "success")
    return redirect(url_for('dashboard.home'))
