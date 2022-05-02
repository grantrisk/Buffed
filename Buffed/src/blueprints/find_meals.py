from flask import Blueprint, render_template, request, redirect, jsonify
from flask_login import login_required, current_user

import firebase_connector
from edamam_connector import EdamamConnector

find_meals_page = Blueprint("find_meals", __name__, static_folder="static", template_folder="templates")

edamam_instance = EdamamConnector()


@find_meals_page.route('/')
@login_required
def find_meals():
    """
    This method returns the find meals page.
    :return: render_template('find_meals.html')
    """
    max_nutrients = firebase_connector.get_remaining_nutrients(current_user.get_id())
    calorie_warn = carbs_warn = protein_warn = fat_warn = False
    if max_nutrients:
        calorie_warn = max_nutrients['calories'] <= 0
        carbs_warn = max_nutrients['carbs'] <= 0
        protein_warn = max_nutrients['protein'] <= 0
        fat_warn = max_nutrients['fat'] <= 0

    return render_template('find_meals.html', calorie_warn=calorie_warn, carbs_warn=carbs_warn,
                           protein_warn=protein_warn, fat_warn=fat_warn)


@find_meals_page.route('/search_results')
@login_required
def search_results():
    """
    Renders the search results page from Find Meals
    :return: HTML content for the search results page
    """
    if 'search_query' not in request.args:
        redirect('find_meals')

    diet = {}

    if 'matchUserDiet' in request.args and request.args['matchUserDiet'] == 'on':
        user = firebase_connector.get_user_info(current_user.get_id())
        if 'diet' in user and len(user['diet']) != 0:
            diet_to_lower = []
            for diet_item in user['diet']:
                diet_to_lower.append(diet_item.lower())
            diet['health'] = diet_to_lower
    elif 'dietSelection' in request.args:
        diet['health'] = request.args.getlist('dietSelection')

    if 'matchUserGoal' in request.args and request.args['matchUserGoal'] == 'on':
        remaining_nutrients = firebase_connector.get_remaining_nutrients(current_user.get_id())
        if remaining_nutrients:
            if remaining_nutrients['calories'] > 0:
                diet['calories'] = remaining_nutrients['calories']
            if remaining_nutrients['carbs'] > 0:
                diet['carbs'] = remaining_nutrients['carbs']
            if remaining_nutrients['protein'] > 0:
                diet['protein'] = remaining_nutrients['protein']
            if remaining_nutrients['fat'] > 0:
                diet['fat'] = remaining_nutrients['fat']

    if 'minCalories' in request.args and request.args['minCalories'] != '':
        min_calories = int(request.args['minCalories'])
        if 'maxCalories' in request.args and request.args['maxCalories'] != '':
            max_calories = int(request.args['maxCalories'])
            if min_calories <= max_calories:
                diet['calories'] = f'{min_calories}-{max_calories}'
            else:
                diet['calories'] = str(min_calories)
        else:
            diet['calories'] = f'{min_calories}+'

    if 'maxCalories' in request.args and request.args['maxCalories'] != '':
        if 'minCalories' not in request.args or ('minCalories' in request.args and request.args['minCalories'] == ''):
            diet['calories'] = request.args['maxCalories']

    if 'minCarbs' in request.args and request.args['minCarbs'] != '':
        min_carbs = request.args['minCarbs']
        if 'maxCarbs' in request.args and request.args['maxCarbs'] != '':
            max_carbs = request.args['maxCarbs']
            if min_carbs <= max_carbs:
                diet['nutrients[CHOCDF]'] = f'{min_carbs}-{max_carbs}'
            else:
                diet['nutrients[CHOCDF]'] = f'{min_carbs}+'
        else:
            diet['nutrients[CHOCDF]'] = f'{min_carbs}+'

    if 'maxCarbs' in request.args and request.args['maxCarbs'] != '':
        if 'minCarbs' not in request.args or ('minCarbs' in request.args and request.args['minCarbs'] == ''):
            diet['nutrients[CHOCDF]'] = request.args['maxCarbs']

    meal_results = edamam_instance.search_recipes(request.args["search_query"], diet)
    saved_meals = firebase_connector.get_all_meals(current_user.get_id())

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
@login_required
def nutrition():
    """
    Renders the Nutrition page for individual meals
    :return: HTML content for the Nutrition page
    """
    if 'meal_id' in request.args:
        meal_id = request.args['meal_id']
        meal = edamam_instance.get_recipe_by_id(meal_id)
        return render_template('nutrition.html', meal=meal, round=round)
    else:
        return redirect('/find_meals')


@find_meals_page.route('/save_meal/', methods=['POST'])
@login_required
def save_meal():
    """
    Handles POST requests for saving meals to a user's account
    :return: POST request response
    """
    if 'id' in request.json:
        meal = edamam_instance.get_recipe_by_id(request.json['id'])
        firebase_connector.save_meal(current_user.get_id(), meal)
        resp = jsonify(success=True)
    else:
        resp = jsonify(success=False)
    return resp


@find_meals_page.route('/remove_meal/', methods=['POST'])
@login_required
def remove_meal():
    """
    Handles POST requests for removing meals from a user's account
    :return: POST request response
    """
    if 'id' in request.json:
        firebase_connector.remove_meal(current_user.get_id(), request.json['id'])
        resp = jsonify(success=True)
    else:
        resp = jsonify(success=False)
    return resp
