from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

# ======= Authentication Forms =======
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

# ======= Task Forms =======
class TaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description")
    assigned_to = StringField("Assign To", validators=[DataRequired()])
    priority = SelectField("Priority", choices=[("High", "High"), ("Medium", "Medium"), ("Low", "Low")], default="Medium")
    status = SelectField("Status", choices=[("Pending", "Pending"), ("In Progress", "In Progress"), ("Completed", "Completed")], default="Pending")
    due_date = DateField("Due Date", format='%Y-%m-%d', validators=[], render_kw={"placeholder": "YYYY-MM-DD"})
    submit = SubmitField("Submit")
