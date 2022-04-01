from flask import Blueprint, render_template, request, url_for, redirect, flash
from firebase_connector import FBConnector
from flask_login import LoginManager
from models import User

index_page = Blueprint("index", __name__, static_folder="static", template_folder="templates")


@index_page.route('/', methods=["GET", "POST"])
@index_page.route('/index', methods=["GET", "POST"])
def index():
    """
    This method returns the index page.
    :return: render_template('index.html')
    """


    # user_dict = FBConnector.get_account_info(FBConnector, "234@gmail.com")

    # name = user_dict['name']
    # email = user_dict['email']
    # weight = user_dict['weight']
    # height = user_dict['height']
    # birth = user_dict['birth']
    # gender = user_dict['gender']
    # current_goal = user_dict['current_goal']
    # print(user_dict)
    # print(user_dict['name'], user_dict['email'])

    # user = User(name, email, weight, height, birth, gender, current_goal)


    if request.method == "POST":

        if 'register-button' in request.form:
            email = request.form["email"]
            confirm_email = request.form["confirm-email"]

            password = request.form["password"]
            confirm_password = request.form["confirm-password"]

            print(email, confirm_email, password, confirm_password)

            if email == confirm_email and password == confirm_password:

                try:
                    FBConnector.register(FBConnector, email, password)
                    # change redirect to profile questionnaire
                    return redirect(url_for("index.index"))

                except:
                    print("Error")
                    return redirect(url_for("index.index"))

            else:
                print("Emails / Password do not match")
                # Stay on this page. Flash toast information user credentials emails/password don't match.

        if 'login-button' in request.form:
            email = request.form["email"]
            password = request.form["password"]

            print(email, password)

            token = FBConnector.sign_in_with_email_and_password(FBConnector, email, password)

            try:
                if token["error"]:
                    # If token has an error. User isn't logged in and can't be authenticated.
                    # User shouldn't move past this page.

                    print("")
                    return redirect(url_for("index.index"))

            except KeyError:
                #
                print(email, password)
                return redirect(url_for("dashboard.dashboard"))

            return redirect(url_for("index.index"))
            # redirect to dashboard

    return render_template('index.html')
