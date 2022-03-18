from flask import Flask, render_template, request
from forms import ContactForm
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_connector import FBConnector

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Flask1WTF2needs3CSRF4'


@app.route('/')
def index():
    """
    This method returns the index page.
    :return: render_template('index.html')
    """
    return render_template('index.html')


@app.route('/login')
def login():
    """
    This method returns the login page.
    :return: render_template('login.html')
    """

    return render_template('login.html')


@app.route('/register')
def register():
    """
        This method returns the register page.
        :return: render_template('register.html')
        """
    return render_template('register.html')


@app.route('/find_meals')
def find_meals():
    """
        This method returns the find meals page.
        :return: render_template('find_meals.html')
        """
    return render_template('find_meals.html')


@app.route('/my_meals')
def my_meals():
    """
        This method returns the my meals page.
        :return: render_template('my_meals.html')
        """
    return render_template('my_meals.html')


@app.route('/dashboard')
def dashboard():
    """
        This method returns the page for the dashboard.
        :return: render_template('dashboard.html')
        """
    return render_template('dashboard.html')


@app.route('/my_goals')
def my_goals():
    """
        This method returns the page my_goals as well as the goals per user.
        :return: render_template('my_goals.html'), goals
        """
    goals = [
        {"id": 1, "name": "bulk", "calories": 4500, "desired_weight": 200, "number_of_meals": 4,
         "protein": [480, 700], "fat": [100, 200], "carbs": [280, 500]},
        {"id": 2, "name": "cut", "calories": 2500, "desired_weight": 155, "number_of_meals": 3,
         "protein": [200, 300], "fat": [50, 100], "carbs": [150, 250]}
    ]
    return render_template('my_goals.html', goals=goals)


@app.route('/my_profile')
def my_profile():
    """
        This method returns the page for my profile.
        :return: render_template('my_profile.html')
        """
    return render_template('my_profile.html')


@app.route('/todays_plan')
def todays_plan():
    """
        This method returns the page for todays_plan.
        :return: render_template('todays_plan.html')
        """
    meals = [
        {"name": "burger", "calories": 400, "protein": 20, "carbs": 250, "fat": 50},
        {"name": "yogurt", "calories": 100, "protein": 5, "carbs": 90, "fat": 40},
        {"name": "pizza", "calories": 300, "protein": 25, "carbs": 200, "fat": 80}
    ]
    return render_template('todays_plan.html', meals=meals)


def send_contact(result):
    pass


@app.route('/about', methods=["GET", "POST"])
def about():
    """
        This method returns the about us page.
        :return: render_template('about.html')
        """
    form = ContactForm()
    if request.method == 'POST':
        result = {'name': request.form["name"],
                  'email': request.form["email"],
                  'subject': request.form["subject"],
                  'message': request.form["message"]}

        send_contact(result)

        return render_template('about.html', form=form)
    else:
        return render_template('about.html', form=form)


@app.route('/create_new_goal')
def create_new_goal():
    """
        This method returns the create new goal page.
        :return: render_template('create_new_goal.html')
    """
    return render_template('create_new_goal.html')



if __name__ == '__main__':
    app.run()
