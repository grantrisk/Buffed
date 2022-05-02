from flask import Blueprint, render_template
from flask_login import login_required, current_user
import firebase_connector as fb
from blueprints import todays_plan

dashboard_page = Blueprint("dashboard", __name__, static_folder="static", template_folder="templates")


@dashboard_page.route('/')
@login_required
def dashboard():
    """
    Renders the Dashboard page
    :return: HTML content for the Dashboard page
    """
    UID = current_user.get_id()
    active_goal = fb.get_user_active_goal(UID)
    if active_goal:
        todays_meals = fb.get_all_meals_todays_plan(UID)
        calories = todays_plan.calculate_totals(todays_meals)
        macrosLabel = []
        macrosVals = []
        macroAvgs = []
        for macro in calories:
            if macro in ("protein", "carbs", "fat"):
                macrosVals.append(round(calories[macro]))
        for i in range(len(macrosVals)):
            macroAvgs.append(float("{:.2f}".format((macrosVals[i] / (sum(macrosVals) + 1)) * 100)))
        return render_template('dashboard.html', goal=active_goal, calories=calories, macrosAvgs=macroAvgs, round=round)
    return render_template('dashboard.html', goal=None)
