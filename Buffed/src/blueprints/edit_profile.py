from flask import Blueprint, render_template

edit_profile_page = Blueprint("edit_profile", __name__, static_folder="static", template_folder="templates")


@edit_profile_page.route('/')
def edit_profile():
    """
        This method returns the page for my profile.
        :return: render_template('my_profile.html')
        """
    return render_template('edit_profile.html')
