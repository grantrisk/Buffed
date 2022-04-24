import uuid

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

import firebase_connector as fb
from models import Meal, MealType

todays_plan_page = Blueprint("todays_plan", __name__, static_folder="static", template_folder="templates")

UID = "hUhfVXJfBxfl2qM0T1trDcs1wdh2"
#meals = fb_connector.get_user_info(UID)['meals']

def calculate_totals(meals):
    """
    This method caluclates the total of all the macros from the meal list in the database
    :return: dictionary of the macros
    """
    total_num_meals = 0
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    for meal in meals:
        total_num_meals += 1
        total_calories += meal.nutrients['ENERC_KCAL']['quantity']
        total_protein += meal.nutrients['PROCNT']['quantity']
        total_carbs += meal.nutrients['CHOCDF']['quantity']
        total_fat += meal.nutrients['FAT']['quantity']
    return {"calories": total_calories, "protein": total_protein, "carbs": total_carbs, "fat": total_fat,
            "num_meals": total_num_meals}


@todays_plan_page.route('/')
@login_required
def todays_plan():
    """
    This method returns the page for todays_plan.
    :return: render_template('todays_plan.html')
    """
    UID = current_user.get_id()
    todays_meals = fb.get_all_meals_todays_plan(UID)
    calories = calculate_totals(todays_meals)
    return render_template('todays_plan.html', meals=todays_meals, calories=calories, round=round)


@todays_plan_page.route('/update_plan/', methods=["POST"])
def update_plan():
    UID = current_user.get_id()
    if request.form['action'] == "Delete":
        meal_id = request.form.get("meal_id")
        meal_type_section = request.form.get("meal_type_section")
        print("Removing " + meal_id + " from " + meal_type_section)
        fb.remove_meal_todays_plan(UID, meal_id, meal_type_section)

    return redirect(url_for('todays_plan.todays_plan'))
