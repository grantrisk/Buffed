from flask import Blueprint, render_template
from flask_login import login_required, current_user
import firebase_connector as fb
import random
from datetime import date

my_profile_page = Blueprint("my_profile", __name__, static_folder="static", template_folder="templates")


@my_profile_page.route('/')
@login_required
def my_profile():
    """
    Renders the My Profile page
    :return: HTML content for the My Profile page
    """
    UID = current_user.get_id()
    user_info = fb.get_user_info(UID)

    greeting_list = ['Howdy', 'Hello', 'Welcome', 'Welcome back', 'How\'s it going', 'Long-time no see',
                     'Yo', 'What\'s up', 'Heyyyyy', 'Sup']
    # Assign a random greeting when they go to the profile page.
    greeting = greeting_list[random.randint(0, 9)]

    # Pull the individual values from the user's dict.
    name = user_info['name']
    weight = user_info['weight']
    height = user_info['height']
    email = user_info['email']
    activity = user_info['activity']
    gender = user_info['gender']
    birthdate = user_info['birth']
    current_goal = user_info['current_goal']

    # Split the user's birthdate into year, month, day
    birth_values = birthdate.split('-')
    year = int(birth_values[0])
    month = int(birth_values[1])
    day = int(birth_values[2])

    # Get the height and then divide to see the ft and then remaining inches.
    ft = str(height // 12) + "'"
    inches = str(height % 12) + "\""

    # Check to see what the age of the person is supposed to be this year
    # If the month, day isn't here yet, just take the age they're supposed to be and minus 1.
    age = date.today().year - year
    month_day_bool = ((date.today().month, date.today().day) < (month, day))

    if month_day_bool:
        age = age - 1
    else:
        age = age
    return render_template('my_profile.html', name=name, weight=weight, ft=ft, inches=inches, email=email,
                           activity=activity, gender=gender, goal=current_goal, greeting=greeting, age=age)
