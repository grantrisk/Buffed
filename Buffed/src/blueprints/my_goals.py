import os
import uuid
from flask import Blueprint, render_template, request
from models import Goal
from firebase_connector import FirebaseConnector
from firebase_admin import firestore
from datetime import date

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
    user = FirebaseConnector.get_user_info(UID)
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

    macro_nutrients = {"carbs": [.35 * (calories * grams)], "fat": [.25 * (calories * grams)],
                       "protein": [.40 * (calories * grams)]}

    standard_goal = Goal(goal_id, goal_name, is_active, round(calories), macro_nutrients, 3, weight)
    FirebaseConnector.create_user_new_goal(UID, standard_goal)


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
        calories = request.form.get("calories")
        macro_nutrients = {"carbs": [request.form.get("carbs")], "fat": [request.form.get("fat")],
                           "protein": [request.form.get("protein")]}
        number_of_meals = request.form.get("number_of_meals")
        desired_weight = request.form.get("desired_weight")
        new_goal = Goal(goal_id, goal_name, is_active, calories, macro_nutrients, number_of_meals, desired_weight)
        # create_standard_goal()
        FirebaseConnector.create_user_new_goal(UID, new_goal)

    # Update Goal
    # goal_doc_ref.update({u'is_active': True})

    goal_doc = get_user_goal_collection().get()
    goalList = []
    for item in goal_doc:
        goalList.append(item.to_dict())
    print(goalList)
    FirebaseConnector.delete_user_goal(UID, u'5e3615dd-2b37-443d-a637-04d8fb8010ee')
    return render_template('my_goals.html', goals=goalList)
