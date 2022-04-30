import flask_login
from flask import Blueprint, render_template, request, url_for, redirect
import firebase_connector as fb_connector
from flask_login import login_user, current_user, login_required

settings_page = Blueprint("settings", __name__, static_folder="static", template_folder="templates")


@settings_page.route('/', methods=['GET', 'POST'])
@login_required
def settings():
    """
        This method returns the page for my profile.
        :return: render_template('my_profile.html')
        """
    UID = current_user.get_id()
    print(UID)
    if request.method == 'POST':
        if 'delete-button' in request.form:
            delete_account = request.form['deleteMe']

            print(delete_account)
            if delete_account == "True":
                fb_connector.delete_user_document(UID)
                fb_connector.delete_user(UID)
                flask_login.logout_user()
                return redirect(url_for('index.index'))

        redirect(url_for('settings.settings'))
    return render_template('settings.html')
