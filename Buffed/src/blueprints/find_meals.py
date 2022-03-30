from flask import Blueprint, render_template, request, redirect

from src import edamam_connector

find_meals_page = Blueprint("find_meals", __name__, static_folder="static", template_folder="templates")


@find_meals_page.route('/find_meals')
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

    meals = edamam_connector.search_recipes(request.args["search_query"])

    return render_template('search_results.html', results=meals, round=round)


@find_meals_page.route('/nutrition')
def nutrition():
    """
    Returns the Nutrition page, which shows an individual meal's nutrition details
    :return: nutrition page template
    """
    if 'meal_id' in request.args:
        meal_id = request.args['meal_id']
        meal = edamam_connector.get_recipe_by_id(meal_id)
        return render_template('nutrition.html', meal=meal, round=round)
    else:
        return redirect('/find_meals')

