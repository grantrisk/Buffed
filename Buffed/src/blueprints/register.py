import flask_login
from flask import Blueprint, render_template, request
from flask_login import current_user

import firebase_connector as FirebaseConnector
from forms import ProfileQuestionnaire

# TODO: need to disable navbar use in setup screen, or move this to index's register module
from models import User

register_page = Blueprint("register", __name__, static_folder="static", template_folder="templates")


def send_info(result):
    """
    Save info to the user object, then send to Firebase connector
    """
    # TODO: Send info to User object to send to Firebase connector
    print("Sending to FB: ", result)

    # how do I get a current user's id?
    # UID = User.get_id()
    UID = current_user.get_id() # email: fake.email@email.com // pass: 123456

    FirebaseConnector.set_user_info(UID, FirebaseEnum.NAME, result.get('name'))
    FirebaseConnector.set_user_info(UID, FirebaseEnum.GENDER, result.get('sex'))
    FirebaseConnector.set_user_info(UID, FirebaseEnum.BIRTH, result.get('birth'))
    FirebaseConnector.set_user_info(UID, FirebaseEnum.WEIGHT, result.get('weight'))
    FirebaseConnector.set_user_info(UID, FirebaseEnum.HEIGHT, result.get('height'))
    FirebaseConnector.set_user_info(UID, FirebaseEnum.ACTIVITY, result.get('activity_lvl'))
    FirebaseConnector.set_user_info(UID, FirebaseEnum.CURRENT_GOAL, result.get('current_goal'))
    FirebaseConnector.set_user_info(UID, FirebaseEnum.DIET, result.get('diet_type'))




@register_page.route('/register', methods=['GET', 'POST'])
def register():
    """
    Render html and pass setup form to html
    """

    profile_form = ProfileQuestionnaire()
    # validate_on_submit checks for submission with POST method,
    # then calls validate() to trigger form validation
    if profile_form.validate_on_submit():
        setup_result = {'name': request.form["name"],
                        'sex': request.form["sex"],
                        'birth': request.form["birth"],
                        'weight': request.form["weight"],
                        'height': request.form["height"],
                        'activity_lvl': request.form["activity_lvl"],
                        'current_goal': request.form["current_goal"],
                        'diet_type': profile_form.diet_type.data}
        # Send this result so it can be stored
        print("Passing on: ", setup_result)
        send_info(setup_result)
        # resume as normal (re-render page with forms after sending)
        return render_template('dashboard.html')
    else:
        # render template with questionnaire form
        return render_template('register.html', profile_form=profile_form)



# we can do this all at once
# @register_page.route('/account_setup', methods=['GET', 'POST'])
# def setup_questions():
#     """
#     Renders both profile and diet questionnaires and gets validated posted info
#     """
#     setup_form = AccountSetupForm()
#
#     # validate_on_submit checks for submission with POST method,
#     # then calls validate() to trigger form validation
#     if "submit" in request.form and setup_form.profile_q.validate(setup_form) and setup_form.diet_q.validate(setup_form):
#         # if a form is posted, store information as result
#         setup_result = {'sex': request.form["sex"],
#                         'bday': request.form["bday"],
#                         'weight': request.form["weight"],
#                         'height': request.form["height"],
#                         'activity_level': request.form["activity_level"],
#                         'goal': request.form["goal"],  # are we using goal objects still?
#                         'diet_type': request.form["diet_type"],
#                         'allergies': request.form["allergies"]}
#         # Send this result so it can be stored
#         print(setup_result)
#         send_info(setup_result)
#         # resume as normal (re-render page with forms after sending)
#         return render_template('register.html', setup_form=setup_form)
#     else:
#         # render template with questionnaire forms
#         return render_template('register.html', setup_form=setup_form)
#
#
# # TODO: not using this for registration currently; should be moved where we'll handle editing information
# @register_page.route('/register-profile', methods=['GET', 'POST'])
# def profile_questions():
#     """
#     This method returns the account setup page.
#     :return: The account setup page including questionnaire forms
#     """
#     profile_form = ProfileQuestionnaire()
#     diet_form = DietQuestionnaire()
#     # validate_on_submit checks for submission with POST method,
#     # then calls validate() to trigger form validation
#     if profile_form.validate_on_submit():
#         # if a form is posted, store information as result
#         profile_result = {'sex': request.form["sex"],
#                           'bday': request.form["bday"],
#                           'weight': request.form["weight"],
#                           'height': request.form["height"],
#                           'activity_level': request.form["activity_level"],
#                           'goal': request.form["goal"]}
#         # Send this result so it can be stored
#         send_info(profile_result)
#         # resume as normal (re-render page with forms after sending)
#         return render_template('register.html', profile_form=profile_form, diet_form=diet_form)
#     else:
#         # render template with questionnaire forms
#         return render_template('register.html', profile_form=profile_form, diet_form=diet_form)
#
#
# # TODO: not using this for registration currently; should be moved where we'll handle editing information
# @register_page.route('/register-diet', methods=['GET', 'POST'])
# def diet_questions():
#     """
#     This method returns the account setup page.
#     :return: The account setup page including questionnaire forms
#     """
#     profile_form = ProfileQuestionnaire()
#     diet_form = DietQuestionnaire()
#
#     # validate_on_submit checks for submission with POST method,
#     # then calls validate() to trigger form validation
#     if diet_form.validate_on_submit():
#         diet_result = {'diet_type': request.form["diet_type"],
#                        'allergies': request.form["allergies"]}
#         # Send this result so it can be stored
#         send_info(diet_result)
#         # resume as normal (re-render page with forms after sending)
#         return render_template('register.html', profile_form=profile_form, diet_form=diet_form)
#     else:
#         # render template with questionnaire forms
#         return render_template('register.html', profile_form=profile_form, diet_form=diet_form)
