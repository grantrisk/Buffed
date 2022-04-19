from flask import Blueprint, render_template, request, redirect, jsonify
from flask_login import login_required, current_user

from firebase_connector import FirebaseConnector
from edamam_connector import EdamamConnector


find_meals_page = Blueprint("find_meals", __name__, static_folder="static", template_folder="templates")

edamam_instance = EdamamConnector()

fb_connector = FirebaseConnector()


@find_meals_page.route('/')
@login_required
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
    if 'search_query' not in request.args:
        redirect('find_meals')

    meal_results = edamam_instance.search_recipes(request.args["search_query"])
    saved_meals = fb_connector.get_all_meals(current_user.get_id())

    results_displayed = []
    saved_results_displayed = []

    if meal_results:
        for meal in meal_results:
            add_meal = True
            for saved_meal in saved_meals:
                if meal.meal_id == saved_meal.meal_id:
                    add_meal = False
                    saved_results_displayed.append(meal)
                    break
            if add_meal:
                results_displayed.append(meal)

    return render_template('search_results.html', saved_meals=saved_results_displayed, results=results_displayed, round=round)


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


@find_meals_page.route('/save_meal/', methods=['POST'])
def save_meal():
    if 'id' in request.json:
        meal = edamam_instance.get_recipe_by_id(request.json['id'])
        fb_connector.save_meal(current_user.get_id(), meal)
        resp = jsonify(success=True)
    else:
        resp = jsonify(success=False)
    return resp


@find_meals_page.route('/remove_meal/', methods=['POST'])
def remove_meal():
    if 'id' in request.json:
        fb_connector.remove_meal(current_user.get_id(), request.json['id'])
        resp = jsonify(success=True)
    else:
        resp = jsonify(success=False)
    return resp
