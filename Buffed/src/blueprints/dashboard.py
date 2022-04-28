from flask import Blueprint, render_template
from flask_login import login_required, current_user
import firebase_connector as fb
from blueprints import todays_plan
from models import *
dashboard_page = Blueprint("dashboard", __name__, static_folder="static", template_folder="templates")


@dashboard_page.route('/')
@login_required
def dashboard():
    """
        This method returns the page for the dashboard.
        :return: render_template('dashboard.html')
    """
    UID = current_user.get_id()
    goalList = fb.get_user_goals(UID)
    todays_meals = fb.get_all_meals_todays_plan(UID)
    calories = todays_plan.calculate_totals(todays_meals)
    for goal in goalList:
        if goal['is_active']:
            active_goal = goal

    return render_template('dashboard.html', goal=active_goal, calories=calories, round=round)
