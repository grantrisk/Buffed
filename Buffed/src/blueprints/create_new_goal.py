from flask import Blueprint, render_template

create_new_goal_page = Blueprint("create_new_goal", __name__, static_folder="static", template_folder="templates")


@create_new_goal_page.route('/')
def create_new_goal():
    """
        This method returns the create new goal page.
        :return: render_template('create_new_goal.html')
    """
    return render_template('create_new_goal.html')
