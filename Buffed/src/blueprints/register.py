from flask_login import current_user, login_user
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

import firebase_connector as fb
from blueprints.index import invalid_credentials_messages
from firebase_connector import FirebaseEnum

from forms import ProfileQuestionnaire, RegisterForm
from blueprints import my_goals
from models import User

register_page = Blueprint("register", __name__, static_folder="static", template_folder="templates")


def send_setup_info(result: dict, UID: str) -> None:
    """
    Save info to the user object, then send to Firebase connector
    """
    # TODO: Remove this print
    print("Sending to FB: ", result)

    fb.set_user_info(UID, FirebaseEnum.NAME, result.get('name'))
    fb.set_user_info(UID, FirebaseEnum.GENDER, result.get('sex'))
    fb.set_user_info(UID, FirebaseEnum.BIRTH, result.get('birth'))
    fb.set_user_info(UID, FirebaseEnum.CURRENT_GOAL, result.get('current_goal'))
    fb.set_user_info(UID, FirebaseEnum.WEIGHT, result.get('weight'))
    fb.set_user_info(UID, FirebaseEnum.HEIGHT, result.get('height'))
    fb.set_user_info(UID, FirebaseEnum.ACTIVITY, result.get('activity'))
    fb.set_user_info(UID, FirebaseEnum.DIET, result.get('diet'))
    standard_goal = my_goals.create_standard_goal(UID)
    fb.create_user_new_goal(UID, standard_goal)


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
    register_form = RegisterForm()
    profile_form = ProfileQuestionnaire()

    if profile_form.submit.data:
        # TODO: securely handle password, other info...
        email = request.form['email']
        confirm_email = request.form['confirm_email']

        password = request.form['password']
        confirm_password = request.form['confirm_password']

        print(email, confirm_email, password, confirm_password)

        if email == confirm_email and password == confirm_password and profile_form.validate_on_submit():
            # validate_on_submit checks for submission with POST method,
            # then calls validate() to trigger form validation
            try:
                fb.create_firebase_account(email, password)
                # ValueError – If the specified user properties are invalid.
                # FirebaseError – If an error occurs while creating the user account.

                response = fb.sign_in_with_email_and_password(email, password)
                if isinstance(response, dict):
                    if "error" in response:
                        if response["error"]["message"] in invalid_credentials_messages:
                            return redirect(url_for('index.index'))
                    elif "kind" in response and response["kind"] == 'identitytoolkit#VerifyPasswordResponse':
                        user_id = response["localId"]
                        token = response["idToken"]
                        expires_in = response["expiresIn"]
                        user = User(user_id, token, expires_in)
                        login_user(user)

                        UID = current_user.get_id()

                        setup_result = {'name': request.form["name"],
                                        'sex': request.form["sex"],
                                        'birth': request.form["birth"],
                                        'current_goal': "Standard Goal",
                                        'weight': request.form["weight"],
                                        'height': calculate_height(request.form["height"]),
                                        'activity': request.form["activity"],
                                        'diet': profile_form.diet_type.data}
                        # Send this result so it can be stored
                        send_setup_info(setup_result, UID)
                        # Go to dashboard
                        return redirect(url_for('dashboard.dashboard'))
            except ValueError:
                # TODO: handle exceptions
                print("Value Error")
                return render_template('register.html', register_form=register_form, profile_form=profile_form)
        else:
            # TODO: Give user feedback
            print("Emails / Passwords do not match")
            return render_template('register.html', register_form=register_form, profile_form=profile_form)
    else:
        # render template with register and profile form
        return render_template('register.html', register_form=register_form, profile_form=profile_form)