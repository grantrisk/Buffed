from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def root():
    """
    This method returns the index page.
    :return: render_template index.html
    """
    return render_template('index.html')


@app.route('/login')
def login():
    """
    This method returns the page for login.
    :return: render_template index.html
    """

    return render_template('login.html')


@app.route('/register')
def register():
    """
    This method returns the page for register.
    :return: render_template register.html
    """
    return render_template('register.html')


@app.route('/find_meals')
def find_meals():
    """
    This method returns the page for find meals.
    :return: render_template find_meals.html
    """
    return render_template('find_meals.html')


@app.route('/my_meals')
def my_meals():
    """
    This method returns the page for my meals.
    :return: render_template index.html
    """
    return render_template('my_meals.html')


@app.route('/dashboard')
def dashboard():
    """
    This method returns the page for dashboard.
    :return: render_template dashboard.html
    """
    return render_template('dashboard.html')


@app.route('/my_goals')
def my_goals():
    """
    This method returns the page for my goals.
    :return: render_template my_goals.html
    """
    return render_template('my_goals.html')


@app.route('/my_profile')
def my_profile():
    """
    This method returns the page for my profile.
    :return: render_template my_profile.html
    """
    return render_template('my_profile.html')


@app.route('/todays_plan')
def todays_plan():
    """
    This method returns the page for today's plan.
    :return: render_template todays_plan.html
    """
    return render_template('todays_plan.html')


@app.route('/about')
def about():
    """
    This method returns the page for the about section.
    :return: render_template about.html
    """
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
