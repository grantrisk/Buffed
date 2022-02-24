from flask import Flask, render_template, url_for

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
    return render_template('my_goals.html')

@app.route('/my_profile')
def my_profile():
    return render_template('my_profile.html')

@app.route('/todays_plan')
def todays_plan():
    return render_template('todays_plan.html')\

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()
