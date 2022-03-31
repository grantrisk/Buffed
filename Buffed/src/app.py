from flask import Flask
from blueprints.todays_plan import todays_plan_page
from blueprints.index import index_page
from blueprints.about import about_page
from blueprints.create_new_goal import create_new_goal_page
from blueprints.dashboard import dashboard_page
from blueprints.find_meals import find_meals_page
from blueprints.login import login_page
from blueprints.my_goals import my_goals_page
from blueprints.my_meals import my_meals_page
from blueprints.my_profile import my_profile_page
from blueprints.register import register_page
from edamam_connector import EdamamConnector

app = Flask(__name__)
app.register_blueprint(index_page, url_prefix='/')
app.register_blueprint(login_page, url_prefix='/login')
app.register_blueprint(register_page, url_prefix='/register')
app.register_blueprint(dashboard_page, url_prefix='/dashboard')
app.register_blueprint(my_goals_page, url_prefix='/my_goals')
app.register_blueprint(create_new_goal_page, url_prefix='/create_new_goal')
app.register_blueprint(find_meals_page, url_prefix='/find_meals')
app.register_blueprint(my_meals_page, url_prefix='/my_meals')
app.register_blueprint(todays_plan_page, url_prefix='/todays_plan')
app.register_blueprint(my_profile_page, url_prefix='/my_profile')
app.register_blueprint(about_page, url_prefix='/about')

config = {}
with open('static/resources/keys.cfg') as file:
    lines = file.readlines()
    for line in lines:
        key_val = line.split('=')
        config[key_val[0].strip()] = key_val[1].strip()

app.config['SECRET_KEY'] = config['flask_wtf']

if __name__ == '__main__':
    app.run()
