from flask import Blueprint, render_template
from flask_login import login_required

from models import Meal
from firebase_connector import FirebaseConnector

todays_plan_page = Blueprint("todays_plan", __name__, static_folder="static", template_folder="templates")

UID = "GiUFl94xwEaQ8VdvIs5QdF0dKy42"
meals = FirebaseConnector().get_user_info(UID)['meals']


@login_required
@todays_plan_page.route('/')
def todays_plan():
    """
    This method returns the page for todays_plan.
    :return: render_template('todays_plan.html')
    """
    return render_template('todays_plan.html', meals=meals)
