import flask_login
from flask import Blueprint, render_template, request, url_for, redirect
import firebase_connector as fb_connector
from flask_login import login_user, current_user

from forms import LoginForm, ContactForm
from models import User, Alert, AlertType

index_page = Blueprint("index", __name__, static_folder="static", template_folder="templates")

invalid_credentials_messages = ['EMAIL_NOT_FOUND', 'INVALID_PASSWORD', 'INVALID_EMAIL']



# Stay on this page. Flash toast information user credentials emails/password don't match.

@index_page.route('/', methods=['GET', 'POST'])
def index():
    """
    This method returns the index page.
    :return: render_template('index.html')
    """
    if request.method == 'GET':
        if "sign_out" in request.args:
            flask_login.logout_user()
        if current_user.get_id() is not None:
            return redirect(url_for("dashboard.dashboard"))
        return render_template('index.html', login_form=LoginForm(), contact_form=ContactForm())
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember_me = request.form['rememberMe']

        print(remember_me)

        response = fb_connector.sign_in_with_email_and_password(email, password)
        if isinstance(response, dict):
            print(response)
            if "error" in response:
                if response["error"]["message"] in invalid_credentials_messages:
                    return {"success": "false"}
                else:
                    return {"success": "error"}
            elif "kind" in response and response["kind"] == 'identitytoolkit#VerifyPasswordResponse':
                user_id = response["localId"]
                token = response["idToken"]
                expires_in = response["expiresIn"]
                user = User(user_id, token, expires_in)

                if remember_me == "True":
                    print(True)
                    login_user(user, remember=True)
                if remember_me == "False":
                    print(False)
                    login_user(user, remember=False)

                return {"success": "true"}
        return {"success": "false"}


@index_page.route('/login_required')
def login_required():
    alerts = [Alert(AlertType.DANGER, "You must be logged in to view this page.")]
    return render_template('index.html', alerts=alerts, login_form=LoginForm(), contact_form=ContactForm())
