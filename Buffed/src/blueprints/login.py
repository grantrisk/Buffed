from flask import Blueprint, render_template

login_page = Blueprint("login", __name__, static_folder="static", template_folder="templates")


@login_page.route('/')
def login():
    """
    This method returns the login page.
    :return: render_template('login.html')
    """

    return render_template('login.html')
