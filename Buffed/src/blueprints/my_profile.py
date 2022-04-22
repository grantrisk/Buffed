from flask import Blueprint, render_template
from flask_login import login_required

my_profile_page = Blueprint("my_profile", __name__, static_folder="static", template_folder="templates")


@my_profile_page.route('/')
@login_required
def my_profile():
    """
        This method returns the page for my profile.
        :return: render_template('my_profile.html')
        """
    return render_template('my_profile.html')
