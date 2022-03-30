from flask import Blueprint, render_template

my_profile_page = Blueprint("my_profile", __name__, static_folder="static", template_folder="templates")


@my_profile_page.route('/')
def my_profile():
    """
        This method returns the page for my profile.
        :return: render_template('my_profile.html')
        """
    return render_template('my_profile.html')
