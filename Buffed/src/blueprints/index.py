import flask_login
from flask import Blueprint, render_template, request, url_for, redirect
import firebase_connector as fb_connector
from flask_login import login_user, current_user

from forms import LoginForm, ContactForm, ForgotPasswordForm
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
    login_form = LoginForm()
    password_reset_email_form = ForgotPasswordForm()

    if request.method == 'GET':
        alerts = []
        if "sign_out" in request.args:
            flask_login.logout_user()
            alerts.append(Alert(AlertType.SUCCESS, "You have been signed out successfully."))
        if current_user.get_id() is not None:
            return redirect(url_for("dashboard.dashboard"))
        return render_template('index.html', alerts=alerts, login_form=LoginForm(), contact_form=ContactForm(),
                               password_reset_email_form=ForgotPasswordForm())

    if login_form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']

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

                try:
                    if request.form['remember_me']:
                        print(True)
                        login_user(user, remember=True)
                except KeyError:
                    print(False)
                    login_user(user, remember=False)

                return {"success": "true"}
        return {"success": "false"}

    if password_reset_email_form.validate_on_submit():
        email = request.form['email']
        fb_connector.reset_user_password(email)
        print("email sent to ", email)
        return redirect(url_for('index.reset_password'))


@index_page.route('/login_required')
def login_required():
    alerts = [Alert(AlertType.DANGER, "You must be logged in to view this page.")]
    return render_template('index.html', alerts=alerts, login_form=LoginForm(), contact_form=ContactForm(),
                           password_reset_email_form=ForgotPasswordForm())


@index_page.route('/deleted_account')
def deleted_account():
    """
    Renders index page and shows alert for successfully deleting an account (redirected from settings)
    """
    alerts = [Alert(AlertType.SUCCESS, "Your account has been successfully deleted.")]
    return render_template('index.html', alerts=alerts, login_form=LoginForm(), contact_form=ContactForm(),
                           password_reset_email_form=ForgotPasswordForm())


@index_page.route('/reset_password')
def reset_password():
    """
    Renders index page and shows alert for successfully requesting
    to reset their password (redirected from index or settings)
    """
    alerts = [Alert(AlertType.SUCCESS, "An email with instructions for resetting your password has been sent.")]
    return render_template('index.html', alerts=alerts, login_form=LoginForm(), contact_form=ContactForm(),
                           password_reset_email_form=ForgotPasswordForm())