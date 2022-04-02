from flask import Blueprint, render_template, request

from forms import ProfileQuestionnaire, DietQuestionnaire

register_page = Blueprint("register", __name__, static_folder="static", template_folder="templates")

@register_page.route('/register')
def register():
    profile_form = ProfileQuestionnaire()
    diet_form = DietQuestionnaire()
    return render_template('register.html', profile_form=profile_form, diet_form=diet_form)


def send_info(result):
    """
    Save info to the user object, then send to Firebase connector
    """
    # TODO: Send info to User object to send to Firebase connector?
    pass


@register_page.route('/register-profile', methods=['GET', 'POST'])
def profile_questions():
    """
        This method returns the account setup page.
        :return: The account setup page including questionnaire forms
        """
    profile_form = ProfileQuestionnaire()
    diet_form = DietQuestionnaire()
    # validate_on_submit checks for submission with POST method,
    # then calls validate() to trigger form validation
    if profile_form.validate_on_submit():
        # if a form is posted, store information as result
        profile_result = {'sex': request.form["sex"],
                          'bday': request.form["bday"],
                          'weight': request.form["weight"],
                          'height': request.form["height"],
                          'activity_level': request.form["activity_level"],
                          'goal': request.form["goal"]}
        # Send this result so it can be stored
        send_info(profile_result)
        # resume as normal (re-render page with forms after sending)
        return render_template('register.html', profile_form=profile_form, diet_form=diet_form)
    else:
        # render template with questionnaire forms
        return render_template('register.html', profile_form=profile_form, diet_form=diet_form)



@register_page.route('/register-diet', methods=['GET', 'POST'])
def diet_questions():
    """
        This method returns the account setup page.
        :return: The account setup page including questionnaire forms
        """
    profile_form = ProfileQuestionnaire()
    diet_form = DietQuestionnaire()

    # validate_on_submit checks for submission with POST method,
    # then calls validate() to trigger form validation
    if diet_form.validate_on_submit():
        diet_result = {'diet_type': request.form["diet_type"],
                       'allergies': request.form["allergies"]}
        # Send this result so it can be stored
        send_info(diet_result)
        # resume as normal (re-render page with forms after sending)
        return render_template('register.html', profile_form=profile_form, diet_form=diet_form)
    else:
        # render template with questionnaire forms
        return render_template('register.html', profile_form=profile_form, diet_form=diet_form)
