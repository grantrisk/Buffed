import flask_login
from flask import Blueprint, render_template, request, url_for, redirect
import firebase_connector as fb
from flask_login import login_user, current_user, login_required
from forms import ConfirmForm

settings_page = Blueprint("settings", __name__, static_folder="static", template_folder="templates")


@settings_page.route('/', methods=['GET', 'POST'])
@login_required
def settings():
    """
        This method returns the page for my profile.
        :return: render_template('my_profile.html')
        """
    UID = current_user.get_id()
    user_info = fb.get_user_info(UID)
    email = user_info['email']

    reset_pw_form = ConfirmForm()

    if reset_pw_form.validate_on_submit():
        fb.reset_user_password(email)
        return redirect(url_for('settings.settings'))

    delete_form = ConfirmForm()

    if delete_form.validate_on_submit():
        delete = delete_form['confirm']
        print(delete)
        fb.delete_user_document(UID)
        fb.delete_user(UID)
        flask_login.logout_user()
        return redirect(url_for('index.index'))

    return render_template('settings.html', delete_form=delete_form, reset_pw_form=reset_pw_form)
