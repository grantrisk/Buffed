from flask import Blueprint, render_template

todays_plan_page = Blueprint("todays_plan", __name__, static_folder="static", template_folder="templates")

@todays_plan_page.route('/')
def todays_plan():
    """
            This method returns the page for todays_plan.
            :return: render_template('todays_plan.html')
            """
    meals = [
        {"name": "burger", "calories": 400, "protein": 20, "carbs": 250, "fat": 50},
        {"name": "yogurt", "calories": 100, "protein": 5, "carbs": 90, "fat": 40},
        {"name": "pizza", "calories": 300, "protein": 25, "carbs": 200, "fat": 80}
    ]
    return render_template('todays_plan.html', meals=meals)