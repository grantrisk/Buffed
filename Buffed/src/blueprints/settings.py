from flask import Blueprint, render_template, request, url_for, redirect
import firebase_connector as fb_connector
from flask_login import login_user, current_user

settings_page = Blueprint("settings", __name__, static_folder="static", template_folder="templates")


@settings_page.route('/', methods=['GET', 'POST'])
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

            print('here')
            if delete_account == "True":
                fb_connector.delete_user(UID)

    return render_template('settings.html')
