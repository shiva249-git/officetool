from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class LoginForm(FlaskForm):
    user_identifier = StringField("Username or Email", validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"autocomplete": "current-password"}
    )
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)],
        render_kw={"autocomplete": "new-password"}
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")],
        render_kw={"autocomplete": "new-password"}
    )
    submit = SubmitField("Register")


class TaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description")
    assigned_to = SelectField("Assign To", coerce=int, validators=[DataRequired()])
    priority = SelectField(
        "Priority",
        choices=[("Low", "Low"), ("Medium", "Medium"), ("High", "High")],
        validators=[DataRequired()]
    )
    status = SelectField(
        "Status",
        choices=[("Pending", "Pending"), ("Completed", "Completed")],
        validators=[DataRequired()]
    )
    due_date = DateField(
        "Due Date",
        format="%Y-%m-%d",
        render_kw={"placeholder": "YYYY-MM-DD"}
    )
    submit = SubmitField("Submit")



class UserEditForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    is_admin = BooleanField("Admin")
    password = PasswordField("New Password (leave blank to keep)", validators=[Optional()])
    submit = SubmitField("Update User")


class LogoutForm(FlaskForm):
    submit = SubmitField("Logout")
