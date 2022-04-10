from flask import Blueprint, render_template
from flask_login import login_required

my_meals_page = Blueprint("my_meals", __name__, static_folder="static", template_folder="templates")


@login_required
@my_meals_page.route('/')
def my_meals():
    """
        This method returns the my meals page.
        :return: render_template('my_meals.html')
        """
    return render_template('my_meals.html')
