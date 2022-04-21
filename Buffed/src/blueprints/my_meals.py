from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

import firebase_connector
from edamam_connector import EdamamConnector

my_meals_page = Blueprint("my_meals", __name__, static_folder="static", template_folder="templates")


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
    if 'id' in request.json:
        firebase_connector.add_to_todays_plan(current_user.get_id(), request.json['id'])
        resp = jsonify(success=True)
    else:
        resp = jsonify(success=False)
    return resp
