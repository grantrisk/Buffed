from flask_login import current_user
from flask import Blueprint, render_template, request, redirect, url_for

import firebase_connector as fb
from firebase_connector import FirebaseEnum

from forms import ProfileQuestionnaire
from blueprints import my_goals

edit_profile_page = Blueprint("edit_profile", __name__, static_folder="static", template_folder="templates")


def send_info(result, UID):
    """
    Save info to the user object, then send to Firebase connector
    """
    print("Sending to FB: ", result)

    # how do I get a current user's id?
    # UID = User.get_id()
    # UID = "aTgX2eI0XLN6CGPiGRacjTOM8g32"  # email: fake.email@email.com // pass: 123456

    fb.set_user_info(UID, FirebaseEnum.NAME, result.get('name'))
    fb.set_user_info(UID, FirebaseEnum.GENDER, result.get('sex'))
    fb.set_user_info(UID, FirebaseEnum.BIRTH, result.get('birth'))
    fb.set_user_info(UID, FirebaseEnum.WEIGHT, result.get('weight'))
    fb.set_user_info(UID, FirebaseEnum.HEIGHT, result.get('height'))
    fb.set_user_info(UID, FirebaseEnum.ACTIVITY, result.get('activity_lvl'))
    fb.set_user_info(UID, FirebaseEnum.CURRENT_GOAL, result.get('current_goal'))
    fb.set_user_info(UID, FirebaseEnum.DIET, result.get('diet_type'))
    my_goals.create_standard_goal(UID)

def calculate_height(height):
    # calculate height in feet
    height = height.split("'")
    return float(height[0]) + float(height[1]) / 12


@edit_profile_page.route('/', methods=['GET', 'POST'])
def edit_profile():
    """
        This method returns the page for my profile.
        :return: render_template('my_profile.html')
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
        return redirect(url_for("my_profile.my_profile"))

    return render_template('edit_profile.html', profile_form=profile_form)
