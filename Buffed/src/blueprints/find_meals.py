from flask import Blueprint, render_template, request, redirect

from src.edamam_connector import EdamamConnector


find_meals_page = Blueprint("find_meals", __name__, static_folder="static", template_folder="templates")

# Temporary - re-parsing config due to problem with circular import trying to access Edamam instance from app.py
# TODO: Make EdamamConnector a Singleton
config = {}
with open('static/resources/keys.cfg') as file:
    lines = file.readlines()
    for line in lines:
        key_val = line.split('=')
        config[key_val[0].strip()] = key_val[1].strip()

edamam_instance = EdamamConnector(config['fd_app_id'], config['fd_app_key'],
                                  config['recipe_app_id'], config['recipe_app_key'],
                                  config['na_app_id'], config['na_app_key'])



@find_meals_page.route('/')
def find_meals():
    """
        This method returns the find meals page.
        :return: render_template('find_meals.html')
        """
    return render_template('find_meals.html')


@find_meals_page.route('/search_results')
def search_results():
    """
    Renders the search results page for Find Meals searches
    :return: search results page template
    """
    if not 'search_query' in request.args:
        redirect('find_meals')

    meals = edamam_instance.search_recipes(request.args["search_query"])

    return render_template('search_results.html', results=meals, round=round)


@find_meals_page.route('/nutrition')
def nutrition():
    """
    Returns the Nutrition page, which shows an individual meal's nutrition details
    :return: nutrition page template
    """
    if 'meal_id' in request.args:
        meal_id = request.args['meal_id']
        meal = edamam_instance.get_recipe_by_id(meal_id)
        return render_template('nutrition.html', meal=meal, round=round)
    else:
        return redirect('/find_meals')

