import flask
import flask_login
from flask import Blueprint, render_template, request, url_for, redirect, flash
from firebase_connector import FirebaseConnector
from flask_login import LoginManager, login_user

from forms import LoginForm
from models import User, Alert, AlertType

index_page = Blueprint("index", __name__, static_folder="static", template_folder="templates")

fb_connector = FirebaseConnector()

invalid_credentials_messages = ['EMAIL_NOT_FOUND', 'INVALID_PASSWORD', 'INVALID_EMAIL']


@index_page.route('/', methods=['GET', 'POST'])
def index():
    """
    This method returns the index page.
    :return: render_template('index.html')
    """
    if request.method == 'GET':
        if "sign_out" in request.args:
            flask_login.logout_user()
        return render_template('index.html')
    elif request.method == 'POST':
        print("POST INCOMING")
        print(request.form)
        email = request.form['email']
        password = request.form['password']
        response = fb_connector.sign_in_with_email_and_password(email, password)
        print(response)
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
                print(login_user)
                return redirect(url_for('dashboard.dashboard'))
        return redirect(url_for('index.index'))


@index_page.route('/login_required')
def login_required():
    alerts = [Alert(AlertType.DANGER, "You must be logged in to view this page.")]
    return render_template('index.html', alerts=alerts, form=LoginForm())
