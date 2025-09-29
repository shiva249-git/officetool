from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import date


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    created_tasks = db.relationship(
        "Task",
        back_populates="creator",
        foreign_keys="Task.user_id",
        lazy=True
    )
    assigned_tasks = db.relationship(
        "Task",
        back_populates="assignee",
        foreign_keys="Task.assigned_to",
        lazy=True
    )

    billings = db.relationship(
        "Billing",
        back_populates="user",
        lazy=True
    )

    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # creator
    assigned_to = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)  # assignee
    status = db.Column(db.String(50), default="Pending")
    priority = db.Column(db.String(50), default="Medium")
    due_date = db.Column(db.Date, nullable=True, default=None)
    deletion_requested = db.Column(db.Boolean, default=False)

    # Relationships
    creator = db.relationship(
        "User",
        back_populates="created_tasks",
        foreign_keys=[user_id]
    )
    assignee = db.relationship(
        "User",
        back_populates="assigned_tasks",
        foreign_keys=[assigned_to]
    )

    def is_editable_by(self, user):
        return user.is_admin or self.user_id == user.id

    def can_delete(self, user):
        """Check if user can delete the task immediately."""
        return user.is_admin or self.user_id == user.id


class Billing(db.Model):
    __tablename__ = "billing"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="Pending")  # Pending / Paid

    user = db.relationship(
        "User",
        back_populates="billings"
    )
