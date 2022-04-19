from flask import Blueprint, render_template

settings_page = Blueprint("settings", __name__, static_folder="static", template_folder="templates")


@settings_page.route('/')
def settings():
    """
        This method returns the page for my profile.
        :return: render_template('my_profile.html')
        """
    return render_template('settings.html')
