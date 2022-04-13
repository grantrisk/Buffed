from flask import Blueprint, render_template
from flask_login import login_required

from models import Meal
from firebase_connector import FirebaseConnector

todays_plan_page = Blueprint("todays_plan", __name__, static_folder="static", template_folder="templates")

UID = "hUhfVXJfBxfl2qM0T1trDcs1wdh2"
meals = FirebaseConnector().get_user_info(UID)['meals']


def calculate_totals():
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    for meal in meals:
        total_calories += meal["nutrients"]["calories"]
        total_protein += meal["nutrients"]["protein"]
        total_carbs += meal["nutrients"]["carbs"]
        total_fat += meal["nutrients"]["fat"]
    return {"calories": total_calories, "protein": total_protein, "carbs": total_carbs, "fat": total_fat, }


# total calories calculated from meals list
calories = calculate_totals()


@login_required
@todays_plan_page.route('/')
def todays_plan():
    """
    This method returns the page for todays_plan.
    :return: render_template('todays_plan.html')
    """
    return render_template('todays_plan.html', meals=meals, calories=calories)
