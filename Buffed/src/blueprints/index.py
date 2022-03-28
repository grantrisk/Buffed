from flask import Blueprint, render_template, request, url_for, redirect, flash
from Buffed.src.firebase_connector import FBConnector

index_page = Blueprint("index", __name__, static_folder="static", template_folder="templates")


@index_page.route('/', methods=["GET", "POST"])
def index():
    """
    This method returns the index page.
    :return: render_template('index.html')
    """

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
