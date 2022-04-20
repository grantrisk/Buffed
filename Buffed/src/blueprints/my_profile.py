from flask import Blueprint, render_template
from flask_login import login_required, current_user
import firebase_connector as fb
import random
my_profile_page = Blueprint("my_profile", __name__, static_folder="static", template_folder="templates")


@login_required
@my_profile_page.route('/')
def my_profile():
    """
        This method returns the page for my profile.
        :return: render_template('my_profile.html')
        """
    UID = current_user.get_id()
    user_info = fb.get_user_info(UID)

    greeting_list = ['Howdy', 'Hello', 'Welcome', 'Welcome back', 'How\'s it going', 'Long-time no see',
                'Yo', 'What\'s up', 'Heyyyyy', 'Sup']

    greeting = greeting_list[random.randint(0, 9)]
    print(user_info)
    print("Greeting: ", greeting)
    name = user_info['name']
    weight = user_info['weight']
    height = user_info['height']
    email = user_info['email']
    activity = user_info['activity']
    gender = user_info['gender']
    current_goal = user_info['current_goal']

    return render_template('my_profile.html', name=name, weight=weight, height=height, email=email,
                           activity=activity, gender=gender, goal=current_goal, greeting=greeting)
