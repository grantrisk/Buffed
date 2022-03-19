from flask import Flask, render_template, request
from forms import ContactForm
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_connector import FBConnector
from blueprints.todays_plan import todays_plan_page

app = Flask(__name__)
app.register_blueprint(todays_plan_page, url_prefix='/todays_plan')

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


def send_contact(result):
    """
        Takes a posted contact email result from about's contact form
        and sends the email.
        :return: None
    """
    # TODO: Implement Contact form functionality that sends email to server?
    # This is for a User Story that's in the icebox currently (noted 3/17/2022)
    pass


@app.route('/about', methods=["GET", "POST"])
def about():
    """
        This method returns the about us page and handles any posted contact form info.
        :return: render_template('about.html')
    """
    form = ContactForm()

    if request.method == 'POST':
        # if an email is posted, store email information as result
        result = {'name': request.form["name"],
                  'email': request.form["email"],
                  'subject': request.form["subject"],
                  'message': request.form["message"]}

        # Send this email result using send_contact method
        send_contact(result)

        # resume as normal (show about.html page with form after sending)
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
