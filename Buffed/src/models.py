from typing import List
from flask_login import UserMixin
from datastore_entity import DatastoreEntity, EntityValue
import datetime


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


class User:
    def __init__(self, name: str, email: str, weight: int, height: int, birth: str, gender: str,
                 current_goal: str):
        self.name = name
        self.email = email
        self.weight = weight
        self.height = weight
        self.birth = birth
        self.gender = gender
        self.current_goal = current_goal

    def get_id(self):
        """
        This method returns the ID (email) of the user.
        """
        return self.email

    def get_name(self):
        """
        This method gets the name of a user from the User object.
        """
        return self.name

    def set_name(self, name):
        """
        This method sets a name for a User object.
        """
        self.name = name

    def get_email(self):
        """
        This method gets the email of a user from the User object.
        """
        return self.email

    def set_email(self, email):
        """
        This method sets the email of a user to a User object.
        """
        self.email = email

    def get_weight(self):
        """
        This method gets the weight of a user from the User object.
        """
        return self.weight

    def set_weight(self, weight):
        """
        This method sets the weight of a user to a User object.
        """
        self.weight = weight

    def get_height(self):
        """
        This method gets the height of a user from the User object.
        """
        return self.height

    def set_height(self, height):
        """
        This method sets the height of a user to a User object.
        """
        self.height = height

    def get_birth(self):
        """
        This method gets the birthdate of a user from a User object.
        """
        return self.birth

    def set_birth(self, birth):
        """
        This method sets the birthdate of a user to a User object.
        """
        self.birth = birth

    def get_gender(self):
        """
        This method gets the gender of a user from a User object.
        """
        return self.gender

    def set_gender(self, gender):
        """
        This method sets the gender of a user to a User object.
        """
        self.gender = gender

    def get_current_goal(self):
        """
        This method gets the current_goal of a user from a User object.
        """
        return self.current_goal

    def set_current_goal(self, current_goal):
        """
        This method sets the current_goal of a user to a User object.
        """
        self.current_goal = current_goal

    def is_authenticated(self):
        return False
