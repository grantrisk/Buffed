from flask import Blueprint, render_template
from src.models import Meal

todays_plan_page = Blueprint("todays_plan", __name__, static_folder="static", template_folder="templates")


meal1 = Meal("burger", "1", "", {"calories":400, "protein":20, "carbs":250, "fat":50}, [], [], [])
meal2 = Meal("yogurt", "2", "", {"calories":100, "protein":5, "carbs":90, "fat":40}, [], [], [])
meal3 = Meal("pizza", "3", "", {"calories":300, "protein":25, "carbs":200, "fat":80}, [], [], [])
meals = [meal1, meal2, meal3]

def delete_meal(meal: Meal):
    """
    Deletes a meal from the dictionary
    :param meal: Meal object
    :return: none
    """
    del meals[meal]


@todays_plan_page.route('/')
def todays_plan():
    """
    This method returns the page for todays_plan.
    :return: render_template('todays_plan.html')
    """
    return render_template('todays_plan.html', meals=meals)
