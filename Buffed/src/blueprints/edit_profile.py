from datetime import datetime

from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, redirect, url_for

import firebase_connector as fb
from firebase_connector import FirebaseEnum

from forms import ProfileQuestionnaire
from blueprints import my_goals

edit_profile_page = Blueprint("edit_profile", __name__, static_folder="static", template_folder="templates")


def send_info(result, UID):
    """
    Sends information edited by the user to Firebase
    :return: None
    """
    fb.set_user_info(UID, FirebaseEnum.NAME, result.get('name'))
    fb.set_user_info(UID, FirebaseEnum.GENDER, result.get('sex'))
    fb.set_user_info(UID, FirebaseEnum.BIRTH, result.get('birth'))
    fb.set_user_info(UID, FirebaseEnum.WEIGHT, result.get('weight'))
    fb.set_user_info(UID, FirebaseEnum.HEIGHT, result.get('height'))
    fb.set_user_info(UID, FirebaseEnum.ACTIVITY, result.get('activity'))
    fb.set_user_info(UID, FirebaseEnum.CURRENT_GOAL, result.get('current_goal'))
    fb.set_user_info(UID, FirebaseEnum.DIET, result.get('diet'))
    my_goals.create_standard_goal(UID)


def calculate_height(ft, inches):
    """
    Parses a user's inputted height, then converts to inches
    :return: int parsed height in inches
    """
    # calculate height in feet
    height_ft = ft.split("'")
    height_in = inches.split("\"")

    ft = int(height_ft[0])
    inches = int(height_in[0])

    ft_to_inches = ft * 12
    total_inches = ft_to_inches + inches
    return total_inches


@edit_profile_page.route('/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Renders the Profile page
    :return: HTML content for the goal creation page
    """
    UID = current_user.get_id()
    user_info = fb.get_user_info(UID)

    # Pull the individual values from the user's dict.
    name = user_info['name']
    weight = user_info['weight']
    height = user_info['height']
    email = user_info['email']
    activity = user_info['activity']
    gender = user_info['gender']
    birthdate = user_info['birth']
    current_goal = user_info['current_goal']
    diet_type = user_info['diet']

    # Split the user's birthdate into year, month, day
    birth_values = birthdate.split('-')
    year = int(birth_values[0])
    month = int(birth_values[1])
    day = int(birth_values[2])

    # Get the height and then divide to see the ft and then remaining inches.
    ft = str(height // 12) + "'"
    inches = str(height % 12) + "\""

    # Convert weight to int
    new_weight = int(weight)

    profile_form = ProfileQuestionnaire()

    # Populate the forms for default values so user doesn't have to re-enter everything.
    if request.method == "GET":
        profile_form.name.data = name
        profile_form.weight.data = int(new_weight)
        profile_form.sex.data = gender
        profile_form.height_feet.data = ft
        profile_form.height_inches.data = inches
        profile_form.activity.data = activity
        profile_form.birth.data = datetime(year, month, day)
        profile_form.diet_type.data = diet_type

    # Validate_on_submit checks for submission with POST method

    # then calls validate() to trigger form validation
    if profile_form.validate_on_submit():
        setup_result = {'name': request.form["name"],
                        'sex': request.form["sex"],
                        'birth': request.form["birth"],
                        'weight': request.form["weight"],
                        'height': calculate_height(request.form["height_feet"], request.form["height_inches"]),
                        'activity': request.form["activity"],
                        'diet': profile_form.diet_type.data,
                        'current_goal': current_goal}

        # Send this result so it can be stored
        send_info(setup_result, UID)

        # Go to profile to see changes on submit
        return redirect(url_for("my_profile.my_profile"))

    return render_template('edit_profile.html', profile_form=profile_form)
