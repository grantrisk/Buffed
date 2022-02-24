from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/find_meals')
def find_meals():
    return render_template('find_meals.html')


@app.route('/my_meals')
def my_meals():
    return render_template('my_meals.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/my_goals')
def my_goals():

    goals = [
        {"id": 1, "name": "bulk", "calories": 4500, "desired_weight": 200, "number_of_meals": 4,
         "protein": [480, 700], "fat": [100, 200], "carbs": [280, 500]},
        {"id": 2, "name": "cut", "calories": 2500, "desired_weight": 155, "number_of_meals": 3,
         "protein": [200, 300], "fat": [50, 100], "carbs": [150, 250]}
    ]
    return render_template('my_goals.html', goals=goals)


@app.route('/my_profile')
def my_profile():
    return render_template('my_profile.html')


@app.route('/todays_plan')
def todays_plan():
    return render_template('todays_plan.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
