from flask import Blueprint, render_template
from forms import MyGoals

create_new_goal_page = Blueprint("create_new_goal", __name__, static_folder="static", template_folder="templates")


@create_new_goal_page.route('/', methods=["GET", "POST"])
def create_new_goal():
    """
        This method returns the create new goal page.
        :return: render_template('create_new_goal.html')
    """
    new_goal_form = MyGoals()
    return render_template('create_new_goal.html', form=new_goal_form)
