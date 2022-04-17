from flask import Blueprint, render_template
from flask_login import login_required, current_user
import firebase_connector as fb
from models import Goal, Meal

dashboard_page = Blueprint("dashboard", __name__, static_folder="static", template_folder="templates")


@login_required
@dashboard_page.route('/')
def dashboard():
    UID = current_user.get_id()
    goalList = fb.get_user_goals(UID)
    """
        This method returns the page for the dashboard.
        :return: render_template('dashboard.html')
        """
    return render_template('dashboard.html', goals=goalList)
