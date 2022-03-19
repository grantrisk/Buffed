from flask import Blueprint, render_template

find_meals_page = Blueprint("find_meals", __name__, static_folder="static", template_folder="templates")


@find_meals_page.route('/')
def find_meals():
    """
        This method returns the find meals page.
        :return: render_template('find_meals.html')
        """
    return render_template('find_meals.html')
