import flask_login
from flask import Blueprint, render_template, request, url_for, redirect
import firebase_connector as fb
from flask_login import current_user, login_required
from forms import ConfirmForm

settings_page = Blueprint("settings", __name__, static_folder="static", template_folder="templates")


@settings_page.route('/', methods=['GET', 'POST'])
@login_required
def settings():
    """
    Shows the settings page and handles forms for password reset and account deletion,
    then redirects the index where it will show appropriate user feedback
    """
    reset_pw_form = ConfirmForm()
    delete_form = ConfirmForm()
    UID = current_user.get_id()

    if request.method == 'POST':
        if 'reset-submit' in request.form and reset_pw_form.validate_on_submit():
            user_info = fb.get_user_info(UID)
            email = user_info['email']
            fb.reset_user_password(email)
            return redirect(url_for('index.reset_password'))
        if 'delete-submit' in request.form and delete_form.validate_on_submit():
            # will only get to this point if the user confirms Yes to delete
            fb.delete_user(UID)
            flask_login.logout_user()
            return redirect(url_for('index.deleted_account'))

    return render_template('settings.html', delete_form=delete_form, reset_pw_form=reset_pw_form)
