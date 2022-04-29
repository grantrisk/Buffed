import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

import firebase_connector as fb
from firebase_admin import firestore

from datetime import date
from models import Goal
from firebase_connector import FirebaseEnum

my_goals_page = Blueprint("my_goals", __name__, static_folder="static", template_folder="templates")


def generate_goal_id():
    goal_id = uuid.uuid4()
    return goal_id


def create_standard_goal(UID: str):
    goal_id = str(generate_goal_id())
    goal_name = "Standard Goal"
    is_active = True
    user = fb.get_user_info(UID)
    height, weight, gender, birthdate, activity_level = user['height'], user['weight'], user['gender'], \
                                                        user['birth'], user['activity']
    birth_values = birthdate.split('-')
    year = int(birth_values[0])
    age = date.today().year - year
    grams = 0.129598
    if gender == "female":
        BMR = 65.51 + (4.35 * int(weight)) + (4.7 * (int(height) * 12)) - (4.7 * age)
    else:
        BMR = 66.47 + (6.24 * int(weight)) + (12.7 * (int(height) * 12)) - (6.75 * age)
    if activity_level == "Very Active":
        calories = BMR * 1.725
    elif activity_level == "Moderately Active":
        calories = BMR * 1.55
    elif activity_level == "Lightly Active":
        calories = BMR * 1.375
    else:
        calories = BMR * 1.2

    macro_nutrients = {"carbs": [int(.35 * (calories * grams))], "fat": [int(.25 * (calories * grams))],
                       "protein": [int(.40 * (calories * grams))]}

    standard_goal = Goal(goal_id, goal_name, is_active, round(calories), macro_nutrients, 3, weight)
    return standard_goal


@my_goals_page.route('/', methods=["GET", "POST"])
@login_required
def my_goals():
    """
        This method returns the page my_goals as well as the goals per user.
        :return: render_template('my_goals.html'), goals
    """
    UID = current_user.get_id()
    if request.method == "POST":
        goal_id = str(generate_goal_id())
        goal_name = request.form.get("goal_name")
        is_active = True
        calories = int(request.form.get("calories"))
        macro_nutrients = {"carbs": [int(request.form.get("carbs"))], "fat": [int(request.form.get("fat"))],
                           "protein": [int(request.form.get("protein"))]}
        number_of_meals = int(request.form.get("number_of_meals"))
        desired_weight = int(request.form.get("desired_weight"))
        new_goal = Goal(goal_id, goal_name, is_active, calories, macro_nutrients, number_of_meals, desired_weight)
        fb.set_active_goal_to_false(UID)
        fb.create_user_new_goal(UID, new_goal)

    goalList = fb.get_user_goals(UID)
    return render_template('my_goals.html', goals=goalList)


@my_goals_page.route('/update_goals/', methods=["POST"])
@login_required
def update_my_goals():
    UID = current_user.get_id()
    if request.form['action'] == "Update":
        active_goal = fb.get_user_active_goal(UID)
        goal_id = request.form.get("goal_id")
        goal_name = request.form.get("goal_name")
        calories = int(request.form.get("calories"))
        macro_nutrients = {"carbs": [int(request.form.get("carbs"))], "fat": [int(request.form.get("fat"))],
                           "protein": [int(request.form.get("protein"))]}
        number_of_meals = int(request.form.get("number_of_meals"))
        desired_weight = int(request.form.get("desired_weight"))
        if request.form.get("active_checkbox") is not None:
            is_active = True
            fb.set_user_info(UID, FirebaseEnum.CURRENT_GOAL, goal_name)
            if active_goal is not None and active_goal['goal_id'] != goal_id:
                fb.set_active_goal_to_false(UID)
        else:
            is_active = False
            if active_goal['goal_id'] == goal_id:
                is_active = True
        updated_goal = Goal(goal_id, goal_name, is_active, calories, macro_nutrients, number_of_meals, desired_weight)
        # Testing standard goal creation for sign up
        # create_standard_goal()
        fb.update_user_goal(UID, updated_goal)

    elif request.form['action'] == "Delete":
        goal_id = request.form.get("goal_id")
        fb.delete_user_goal(UID, goal_id)

    return redirect(url_for('my_goals.my_goals'))