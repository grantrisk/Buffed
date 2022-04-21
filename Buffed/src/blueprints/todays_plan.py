import uuid

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

import firebase_connector as fb
from models import Meal, MealType

todays_plan_page = Blueprint("todays_plan", __name__, static_folder="static", template_folder="templates")


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
        total_calories += meal.nutrients['calories']
        total_protein += meal.nutrients["protein"]
        total_carbs += meal.nutrients["carbs"]
        total_fat += meal.nutrients["fat"]
    return {"calories": total_calories, "protein": total_protein, "carbs": total_carbs, "fat": total_fat,
            "num_meals": total_num_meals}


@login_required
@todays_plan_page.route('/')
def todays_plan():
    """
    This method returns the page for todays_plan.
    :return: render_template('todays_plan.html')
    """
    UID = current_user.get_id()
    todays_meals = fb.get_all_meals_todays_plan(UID)
    calories = calculate_totals(todays_meals)
    return render_template('todays_plan.html', meals=todays_meals, calories=calories)


@todays_plan_page.route('/update_plan/', methods=["POST"])
def update_plan():
    UID = current_user.get_id()
    if request.form['action'] == "Delete":
        meal_id = request.form.get("meal_id")
        fb.remove_meal_todays_plan(UID, meal_id)
    elif request.form['action'] == "Add":
        meal1 = Meal("burger", str(uuid.uuid4()), MealType.DINNER.value, "",
                     {"calories": 400, "protein": 20, "carbs": 250, "fat": 50}, [], [], [])
        fb.add_meal_todays_plan(UID, meal1)

    return redirect(url_for('todays_plan.todays_plan'))
