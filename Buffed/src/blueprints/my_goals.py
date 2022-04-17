import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for
from models import Goal
import firebase_connector as fb_connector
from firebase_admin import firestore
from datetime import date
from flask import Blueprint, render_template
from flask_login import login_required

my_goals_page = Blueprint("my_goals", __name__, static_folder="static", template_folder="templates")
# Temporary Direct Access to Firestore
db = firestore.client()
# Temporary Hard-Coded UserID
UID = "VS8kx0L0DJVXhBEev86LyxUZpZb2"


def generate_goal_id():
    goal_id = uuid.uuid4()
    return goal_id


def create_standard_goal():
    goal_id = str(generate_goal_id())
    goal_name = "Standard Goal"
    is_active = True
    user = fb_connector.get_user_info(UID)
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
    fb_connector.create_user_new_goal(UID, standard_goal)


@login_required
@my_goals_page.route('/', methods=["GET", "POST"])
def my_goals():
    """
        This method returns the page my_goals as well as the goals per user.
        :return: render_template('my_goals.html'), goals
    """

    def get_user_goal_collection():
        goal_doc_ref = db.collection(u'users').document(UID).collection(u'savedGoals')
        return goal_doc_ref

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
        # Testing standard goal creation for sign up
        # create_standard_goal()
        fb_connector.create_user_new_goal(UID, new_goal)

    # Update Goal
    # goal_doc_ref.update({u'is_active': True})

    goal_doc = get_user_goal_collection().get()
    goalList = []
    for item in goal_doc:
        goalList.append(item.to_dict())
    # Temporarily deleting old goals
    # FirebaseConnector.delete_user_goal(UID, u'06270fac-be35-44d6-a2bc-c6e5646aba88')
    return render_template('my_goals.html', goals=goalList)


@my_goals_page.route('/update_goals/', methods=["GET", "POST"])
def update_my_goals():

    if request.method == "POST":
        goal_id = request.form.get("goal_id")
        goal_name = request.form.get("goal_name")
        is_active = True
        calories = int(request.form.get("calories"))
        macro_nutrients = {"carbs": [int(request.form.get("carbs"))], "fat": [int(request.form.get("fat"))],
                           "protein": [int(request.form.get("protein"))]}
        number_of_meals = int(request.form.get("number_of_meals"))
        desired_weight = int(request.form.get("desired_weight"))
        updated_goal = Goal(goal_id, goal_name, is_active, calories, macro_nutrients, number_of_meals, desired_weight)
        # Testing standard goal creation for sign up
        # create_standard_goal()
        fb_connector.update_user_goal(UID, updated_goal)
        return redirect(url_for('my_goals.my_goals'))