from flask import Blueprint, render_template
from forms import MyGoals

create_new_goal_page = Blueprint("create_new_goal", __name__, static_folder="static", template_folder="templates")


@create_new_goal_page.route('/', methods=["GET", "POST"])
def create_new_goal():
    """
    Renders the goal creation page
    :return: HTML content for the goal creation page
    """
    new_goal_form = MyGoals()
    return render_template('create_new_goal.html', form=new_goal_form)
