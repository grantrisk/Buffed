import flask_login
from flask_login import current_user
from flask import Blueprint, render_template, request

import firebase_connector as fb
from firebase_connector import FirebaseEnum

from forms import ProfileQuestionnaire
from blueprints import my_goals

register_page = Blueprint("register", __name__, static_folder="static", template_folder="templates")


def send_info(result: dict, UID: str) -> None:
    """
    Save info to the user object, then send to Firebase connector
    """

    print("Sending to FB: ", result)

    fb.set_user_info(UID, FirebaseEnum.NAME, result.get('name'))
    fb.set_user_info(UID, FirebaseEnum.GENDER, result.get('sex'))
    fb.set_user_info(UID, FirebaseEnum.BIRTH, result.get('birth'))
    fb.set_user_info(UID, FirebaseEnum.WEIGHT, result.get('weight'))
    fb.set_user_info(UID, FirebaseEnum.HEIGHT, result.get('height'))
    fb.set_user_info(UID, FirebaseEnum.ACTIVITY, result.get('activity'))
    fb.set_user_info(UID, FirebaseEnum.DIET, result.get('diet'))
    my_goals.create_standard_goal(UID)  # create a new standard goal and set it as current goal


def calculate_height(height: str) -> float:
    """
    Calculate height in feet as a float
    :param height: string formatted as feet-inches (6'2)
    :return: height in feet
    """
    height = height.split("'")
    return float(height[0]) + float(height[1]) / 12


@register_page.route('/', methods=['GET', 'POST'])
def register():
    """
    Render html and pass setup form to html
    """
    UID = current_user.get_id()
    profile_form = ProfileQuestionnaire()
    # validate_on_submit checks for submission with POST method,
    # then calls validate() to trigger form validation
    if profile_form.validate_on_submit():
        setup_result = {'name': request.form["name"],
                        'sex': request.form["sex"],
                        'birth': request.form["birth"],
                        'weight': request.form["weight"],
                        'height': calculate_height(request.form["height"]),
                        'activity': request.form["activity"],
                        'diet': profile_form.diet_type.data}
        # Send this result so it can be stored
        print("Passing on: ", setup_result)
        send_info(setup_result, UID)
        # Go to dashboard
        return render_template('dashboard.html')
    else:
        # render template with questionnaire form
        return render_template('register.html', profile_form=profile_form)