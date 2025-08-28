from flask import Blueprint, render_template, session, redirect, url_for

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/")
def home():
    if "user_email" not in session:
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html", user_email=session["user_email"])
