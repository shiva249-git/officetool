from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import date


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Tasks created by this user (author/creator)
    created_tasks = db.relationship(
        "Task",
        backref="creator",
        lazy=True,
        foreign_keys="Task.user_id"
    )

    # Tasks assigned to this user
    assigned_tasks = db.relationship(
        "Task",
        backref="assignee",
        lazy=True,
        foreign_keys="Task.assigned_to"
    )

    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # creator
    assigned_to = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)  # assignee
    status = db.Column(db.String(50), default="Pending")
    priority = db.Column(db.String(50), default="Medium")
    due_date = db.Column(db.Date, nullable=True, default=None)
    deletion_requested = db.Column(db.Boolean, default=False)

    assigned_user = db.relationship("User", foreign_keys=[assigned_to], backref="tasks_assigned_to")

    def is_editable_by(self, user):
        return user.is_admin or self.user_id == user.id

    def can_delete(self, user):
        """Check if user can delete the task immediately."""
        return user.is_admin or self.user_id == user.id
