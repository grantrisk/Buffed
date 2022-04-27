from firebase_admin._auth_utils import EmailAlreadyExistsError
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


# def handle_catch(caller, on_exception):
#     """
#     Try statement to include in register.html macro
#     :param caller:
#     """
#     try:
#         return caller()
#     except:
#         return on_exception
#
#
# def check_email(email):
#     """
#     Try statement to include in register.html macro
#     :param email: the given email
#     :return errorMsg: the error message to show or an empty string
#     """
#     pass
#     # try:
#     #     emailObject = validate_email(email)
#     #     t
#     # except:
#     #     return on_exception

@register_page.route('/', methods=['GET', 'POST'])
def register():
    """
    Render html and pass setup form to html
    """
    register_form = RegisterForm()
    profile_form = ProfileQuestionnaire()

    if profile_form.submit.data and register_form.validate():
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
                                        'weight': request.form["weight"],
                                        'height': calculate_height(request.form["height"]),
                                        'activity': request.form["activity"],
                                        'diet': profile_form.diet_type.data}
                        # Send this result so it can be stored
                        send_setup_info(setup_result, UID)
                        # Go to dashboard
                        return render_template('dashboard.html')
            except EmailAlreadyExistsError as errorMsg:
                return render_template('register.html', register_form=register_form, profile_form=profile_form, error=str(errorMsg))
            except ValueError:
                # TODO: handle exceptions
                print("Value Error")
                return render_template('register.html', register_form=register_form, profile_form=profile_form)
        else:
            return render_template('register.html', register_form=register_form, profile_form=profile_form)
    else:
        # render template with register and profile form
        return render_template('register.html', register_form=register_form, profile_form=profile_form)