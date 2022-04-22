from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

import firebase_connector
from edamam_connector import EdamamConnector
from models import MealType

my_meals_page = Blueprint("my_meals", __name__, static_folder="static", template_folder="templates")

edamam_instance = EdamamConnector()


@my_meals_page.route('/')
@login_required
def my_meals():
    """
    This method returns the my meals page.
    :return: render_template('my_meals.html')
    """
    return render_template('my_meals.html', saved_meals=firebase_connector.get_all_meals(current_user.get_id()),
                           round=round)


@my_meals_page.route('/add_to_plan/', methods=['POST'])
@login_required
def add_to_todays_plan():
    """
    Used for AJAX POST requests to save a given meal to Today's Plan
    :return: success status
    """
    if 'mealID' in request.form and 'mealTypeOption' in request.form:
        meal = edamam_instance.get_recipe_by_id(request.form['mealID'])
        meal.meal_type_section = request.form['mealTypeOption']
        firebase_connector.add_meal_todays_plan(current_user.get_id(), meal)
        resp = jsonify(success=True)
    else:
        resp = jsonify(success=False)
    return resp
