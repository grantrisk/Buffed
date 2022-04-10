import time
from enum import Enum
from typing import List

from flask_login import UserMixin


class User(UserMixin):
    """
    Object used for flask-login authentication. Stores a user's ID, session token, and token expiration time.
    """
    # Dictionary to store active user sessions. Elements stored in {"user_id": User} format.
    active_users = {}

    @classmethod
    def get(cls, user_id):
        """
        Fetches a User object from the active_users variable
        :param user_id:
        :return:
        """
        if user_id in cls.active_users:
            return cls.active_users[user_id]

    def __init__(self, user_id, session_token, exp_time):
        """
        Creates an instance of a User object.
        :param user_id: user's unique ID
        :param session_token: user's session token
        :param exp_time: user's session token expiration time in seconds
        """
        self.__user_id = user_id
        self.__session_token = session_token
        try:
            self.__exp_time = time.time() + int(exp_time)
        except ValueError:
            print("Expire time is invalid. Value: " + exp_time + ". Aborting login.")
            self.__exp_time = 0

        User.active_users[user_id] = self

    def is_authenticated(self):
        if time.time() < self.__exp_time:
            User.active_users.pop(self.__user_id)
            return False
        return True

    def is_active(self):
        return self.is_authenticated()

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.__user_id


class Measure:
    """
    Object representation of a measure, used internally for Ingredient nutrition lookup
    """

    def __init__(self, measure_label, measure_uri, weight):
        self.measure_label = measure_label
        self.measure_uri = measure_uri
        self.weight = weight


class Ingredient:
    def __init__(self, ingredient_name: str, ingredient_id: str, ingredient_img_url: str, ingredient_nutrients: dict,
                 ingredient_health_labels: List[str], ingredient_measures: List[Measure]):
        """
        Creates an instance of an Ingredient object
        :param ingredient_name: name of the ingredient
        :param ingredient_id: unique identifier of the ingredient from Edamam
        :param ingredient_img_url: URL to the ingredient image from Edamam
        :param ingredient_nutrients: dictionary containing the ingredient nutritional values (per 100 grams)
        :param ingredient_health_labels: list containing all ingredient health labels as defined by Edamam
        """
        self.ingredient_name = ingredient_name
        self.ingredient_id = ingredient_id
        self.ingredient_img_url = ingredient_img_url
        self.ingredient_nutrients = ingredient_nutrients
        self.ingredient_health_labels = ingredient_health_labels
        self.ingredient_measures = ingredient_measures


class Meal:
    def __init__(self, meal_name: str, meal_id: str, meal_img_url, nutrients: dict, health_labels: List[str],
                 ingredients: List[str], meal_types: List[str]):
        """
        Creates an instance of a Meal object
        :param meal_name: name of the meal
        :param meal_id: unique identifier for the Meal
        :param meal_img_url: URL to image of meal
        :param nutrients: dictionary containing all nutrients
        :param health_labels: list containing all health labels as defined by Edamam
        :param ingredients: list containing all ingredients in the meal
        :param meal_types: type of meal (i.e. Breakfast, Lunch, Dinner, etc.)
        """
        self.meal_name = meal_name
        self.meal_id = meal_id
        self.meal_img_url = meal_img_url
        self.nutrients = nutrients
        self.health_labels = health_labels
        self.ingredients = ingredients
        self.meal_type = meal_types

    def get_name(self):
        return self.meal_name

    def get_nutrients(self):
        return self.nutrients


class Goal:
    def __init__(self, goal_id: str, goal_name: str, is_active: bool, calories: int, macro_nutrients: dict,
                 number_of_meals: int, desired_weight: int):
        """
        Creates an instance of a Goal object
        :param goal_id: unique identifier for Goal stored in Firebase
        :param goal_name: name of the goal
        :param is_active: determines active goal
        :param calories: daily calorie amount to achieve
        :param macro_nutrients: dictionary containing protein, fat, and carb amounts (g)
        :param number_of_meals: number of desired meals per day
        :param desired_weight: desired weight to achieve (lbs)
        """
        self.goal_id = goal_id
        self.goal_name = goal_name
        self.is_active = is_active
        self.calories = calories
        self.macro_nutrients = macro_nutrients
        self.number_of_meals = number_of_meals
        self.desired_weight = desired_weight


class MealPlan:
    def __init__(self, user_id: str, meals: List[Meal]):
        """
        Creates an instance of a MealPlan object.
        :param user_id: the ID of the user who owns the MealPlan
        :param meals: the list of Meal objects for the meal plan, associated with the user object
        """
        self.user_id = user_id
        self.meals = meals


class AlertType(Enum):
    PRIMARY = 'alert-primary'
    SECONDARY = 'alert-secondary'
    SUCCESS = 'alert-success'
    DANGER = 'alert-danger'
    WARNING = 'alert-warning'
    INFO = 'alert-info'
    LIGHT = 'alert-light'
    DARK = 'alert-dark'


class Alert:
    def __init__(self, alert_type: AlertType, message: str):
        """
        Creates an instance of an Alert
        :param alert_type: AlertType, alert style
        :param message: message to be displayed in the alert
        """
        self.alert_type = alert_type
        self.message = message

