from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import User

import firebase_connector as fb

todays_plan_page = Blueprint("todays_plan", __name__, static_folder="static", template_folder="templates")


def calculate_totals(meals):
    """
    This method caluclates the total of all the macros from the meal list in the database
    :return: dictionary of the macros
    """
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


@login_required
@todays_plan_page.route('/')
def todays_plan():
    """
    This method returns the page for todays_plan.
    :return: render_template('todays_plan.html')
    """
    # UID = current_user.get_id()
    UID = "hUhfVXJfBxfl2qM0T1trDcs1wdh2"
    meals = fb.get_user_info(UID)['meals']
    calories = calculate_totals(meals)
    return render_template('todays_plan.html', meals=meals, calories=calories)

@todays_plan_page.route('/update_plan/', methods=["POST"])
def update_plan():
    UID = current_user.get_id()
    if request.form['action'] == "Delete":
        meal_id = request.form.get("meal_id")
        fb.delete_meal(UID, meal_id)

    return redirect(url_for('todays_plan.todays_plan'))
