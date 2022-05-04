import time
from enum import Enum
from typing import List

from flask_login import UserMixin


class User(UserMixin):
    """
    Object used for flask-login authentication. Stores a user's ID.
    """

    @classmethod
    def get(cls, user_id):
        """
        Fetches a User object from the active_users variable
        :param user_id:
        :return:
        """
        return User(user_id)

    def __init__(self, user_id):
        """
        Creates an instance of a User object.
        :param user_id: user's unique ID
        :param session_token: user's session token
        :param exp_time: user's session token expiration time in seconds
        """
        self.__user_id = user_id

    def is_authenticated(self):
        return True

    def is_active(self):
        """
        Determines if a user is active. A user is active if they are authenticated.
        :return: True if authenticated, False otherwise
        """
        return self.is_authenticated()

    def is_anonymous(self):
        """
        Determines if a user is logged in anonymously. Buffed does not support anonymous logins, so will retuirn False.
        :return: False
        """
        return False

    def get_id(self):
        """
        Getter method for a user's ID
        :return: user ID
        """
        return self.__user_id

    def to_json(self):
        return {'user_id': self.__user_id}

    @classmethod
    def from_json(cls, json):
        return User(json['user_id'])


class Measure:
    """
    Object representation of a measure, used internally for Ingredient nutrition lookup
    """
    def __init__(self, measure_label, measure_uri, weight):
        """
        Creates an instance of a Measure object
        :param measure_label: display name for the measure
        :param measure_uri: Edamam URI for measure
        :param weight: weight in grams
        """
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


class MealType(Enum):
    """
    Enum for Meal Type storage in Firebase
    """
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"


class Meal:
    def __init__(self, meal_name: str, meal_id: str, meal_type_section: str, meal_img_url, nutrients: dict, health_labels: List[str],
                 ingredients: List[str], meal_types: List[str], recipe_source: str, recipe_url: str):
        """
        Creates an instance of a Meal object
        :param meal_name: name of the meal
        :param meal_id: unique identifier for the Meal
        :param meal_type_section: Enum string of MealType
        :param meal_img_url: URL to image of meal
        :param nutrients: dictionary containing all nutrients
        :param health_labels: list containing all health labels as defined by Edamam
        :param ingredients: list containing all ingredients in the meal
        :param meal_types: type of meal (i.e. Breakfast, Lunch, Dinner, etc.)
        :param recipe_source: name of source of recipe, provided by Edamam
        :param recipe_url: URL to recipe, provided by Edamam
        """
        self.meal_name = meal_name
        self.meal_id = meal_id
        self.meal_type_section = meal_type_section
        self.meal_img_url = meal_img_url
        self.nutrients = nutrients
        self.health_labels = health_labels
        self.ingredients = ingredients
        self.meal_types = meal_types
        self.recipe_source = recipe_source
        self.recipe_url = recipe_url

    def to_json(self):
        """
        Converts Meal object into a dictionary
        :return: a dictionary
        """
        return vars(self)

    @classmethod
    def from_dict(cls, data: dict):
        """
        Class method to convert dictionary to Meal object
        :param data: dictionary containing meal data
        :return: a Meal object
        """
        return Meal(data['meal_name'], data['meal_id'], data['meal_type_section'], data['meal_img_url'], data['nutrients'],
                    data['health_labels'], data['ingredients'], data['meal_types'], data['recipe_source'], data['recipe_url'])


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

    def __eq__(self, other):
        if isinstance(other, Goal):
            return self.goal_name == other.goal_name and self.calories == other.calories


class AlertType(Enum):
    """
    Enum used for alert types in Bootstrap
    """
    PRIMARY = 'alert-primary'
    SECONDARY = 'alert-secondary'
    SUCCESS = 'alert-success'
    DANGER = 'alert-danger'
    WARNING = 'alert-warning'
    INFO = 'alert-info'
    LIGHT = 'alert-light'
    DARK = 'alert-dark'


class Alert:
    """
    Object used for Bootstrap alerts
    """
    def __init__(self, alert_type: AlertType, message: str):
        """
        Creates an instance of an Alert
        :param alert_type: AlertType, alert style
        :param message: message to be displayed in the alert
        """
        self.alert_type = alert_type
        self.message = message
