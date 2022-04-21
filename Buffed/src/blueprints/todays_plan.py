from flask import Blueprint, render_template
from flask_login import login_required

from models import Meal
import firebase_connector as fb_connector

todays_plan_page = Blueprint("todays_plan", __name__, static_folder="static", template_folder="templates")

UID = "hUhfVXJfBxfl2qM0T1trDcs1wdh2"
#meals = fb_connector.get_user_info(UID)['meals']


@todays_plan_page.route('/')
@login_required
def todays_plan():
    """
    This method returns the page for todays_plan.
    :return: render_template('todays_plan.html')
    """
    return render_template('todays_plan.html', meals=meals)
