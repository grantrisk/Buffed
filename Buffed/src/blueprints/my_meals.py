from flask import Blueprint, render_template

my_meals_page = Blueprint("my_meals", __name__, static_folder="static", template_folder="templates")


@my_meals_page.route('/')
def my_meals():
    """
        This method returns the my meals page.
        :return: render_template('my_meals.html')
        """
    return render_template('my_meals.html')
