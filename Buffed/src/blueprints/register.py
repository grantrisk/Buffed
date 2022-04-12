from flask import Blueprint, render_template, request

from forms import ProfileQuestionnaire

# TODO: need to disable navbar use in setup screen, or move this to index's register module
register_page = Blueprint("register", __name__, static_folder="static", template_folder="templates")


def send_info(result):
    """
    Save info to the user object, then send to Firebase connector
    """
    # TODO: Send info to User object to send to Firebase connector
    print(result)


@register_page.route('/register', methods=['GET', 'POST'])
def register():
    """
    Render html and pass setup form to html
    """

    profile_form = ProfileQuestionnaire()

    # validate_on_submit checks for submission with POST method,
    # then calls validate() to trigger form validation
    if profile_form.validate_on_submit():
        # if form is posted, store information as result
        setup_result = {'sex': request.form["sex"],
                        'bday': request.form["bday"],
                        'weight': request.form["weight"],
                        'height': request.form["height"],
                        'activity_lvl': request.form["activity_lvl"],
                        'diet_type': profile_form.diet_type.data}
        # Send this result so it can be stored
        send_info(setup_result)
        # resume as normal (re-render page with forms after sending)
        return render_template('dashboard.html')
    else:
        # render template with questionnaire forms
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
