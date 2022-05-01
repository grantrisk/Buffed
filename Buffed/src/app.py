from flask import Flask
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from blueprints.todays_plan import todays_plan_page
from blueprints.index import index_page
from blueprints.about import about_page
from blueprints.create_new_goal import create_new_goal_page
from blueprints.dashboard import dashboard_page
from blueprints.find_meals import find_meals_page
from blueprints.my_goals import my_goals_page
from blueprints.my_meals import my_meals_page
from blueprints.my_profile import my_profile_page
from blueprints.register import register_page
from blueprints.edit_profile import edit_profile_page
from blueprints.settings import settings_page

from models import User

app = Flask(__name__, static_url_path='/static')
limiter = Limiter(app, key_func=get_remote_address, default_limits=['75 per minute'])

app.register_blueprint(index_page, url_prefix='/')
app.register_blueprint(register_page, url_prefix='/register')
app.register_blueprint(dashboard_page, url_prefix='/dashboard')
app.register_blueprint(my_goals_page, url_prefix='/my_goals')
app.register_blueprint(create_new_goal_page, url_prefix='/create_new_goal')
app.register_blueprint(find_meals_page, url_prefix='/find_meals')
app.register_blueprint(my_meals_page, url_prefix='/my_meals')
app.register_blueprint(todays_plan_page, url_prefix='/todays_plan')
app.register_blueprint(my_profile_page, url_prefix='/my_profile')
app.register_blueprint(about_page, url_prefix='/about')
app.register_blueprint(edit_profile_page, url_prefix='/edit_profile')
app.register_blueprint(settings_page, url_prefix='/settings')

config = {}
with open('static/resources/keys.cfg') as file:
    lines = file.readlines()
    for line in lines:
        key_val = line.split('=')
        config[key_val[0].strip()] = key_val[1].strip()

app.config['SECRET_KEY'] = config['flask_wtf']

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index.login_required'


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


if __name__ == '__main__':
    app.run(debug=True)
