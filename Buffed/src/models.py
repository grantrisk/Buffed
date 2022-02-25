from typing import List


class Meal:
    def __init__(self, food_name: str, food_id: str, img_url: str, nutrients: dict, health_labels: List[str]):
        """
        Creates an instance of a Meal object
        :param food_name: name of the food
        :param food_id: unique identifier of the food from Edamam
        :param img_url: URL to the image from Edamam
        :param nutrients: dictionary containing the nutritional values
        :param health_labels: list containing all health labels as defined by Edamam
        """
        self.food_name = food_name
        self.food_id = food_id
        self.img_url = img_url
        self.nutrients = nutrients
        self.health_labels = health_labels


class Goal:
    def __init__(self, fats: List[float, float], carbs: List[float, float], protein: List[float, float]):
        """
        Creates an instance of a Goal object
        :param fats: a list of gaol high and low ranges for fats
        :param carbs: a list of gaol high and low ranges for carbs
        :param protein: a list of gaol high and low ranges for protein
        """
        self.fats = fats
        self.carbs = carbs
        self.protein = protein


class User:
    def __init__(self, email: str, password: str, name: str, birthdate: str, gender: str,
                 weight: float, height: float, activity_level: str, active_goal: Goal, keywords: List[str],
                 allergies: List[str], diet_preferences: List[str], likes: List[str], dislikes: List[str],
                 my_meals: List[Meal], my_goals: List[Goal]):
        """
        Creates an instance of a User object
        :param email: user's email
        :param password: user's password
        :param name: user's display name
        :param birthdate: user's birthdate for age calculation
        :param gender: user's gender
        :param weight: user's weight in lbs
        :param height: user's height in meters
        :param activity_level: user's activity level
        :param active_goal: user's active or current goal
        :param keywords: list of the user's favorite ingredients/food keywords from Firestore
        :param allergies: list of the user's allergies from Firestore
        :param diet_preferences: list of the user's diet preferences from Firestore
        :param likes: list of the user's likes from Firestore
        :param dislikes: list of the user's dislikes from Firestore
        :param my_meals: list of Meal objects that the user has saved from My Meals
        :param my_goals: list of goals including fat, carbs, and protein values' high and low ranges
        """
        self.email = email
        self.password = password
        self.name = name
        self.birthdate = birthdate
        self.gender = gender
        self.weight = weight
        self.height = height
        self.activity_level = activity_level
        self.active_goal = active_goal
        self.keywords = keywords
        self.allergies = allergies
        self.diet_preferences = diet_preferences
        self.likes = likes
        self.dislikes = dislikes
        self.my_meals = my_meals
        self.my_goals = my_goals


class MealPlan:
    def __init__(self, user: User, meals: List[Meal]):
        """
        Creates an instance of a MealPlan object.
        :param user: the user's object
        :param meals: the list of Meal objects for the meal plan, associated with the user object
        """
        self.user = user
        self.meals = meals


class Ingredient:
    def __init__(self, ingredient_name: str, ingredient_id: str, ingredient_img_url: str, ingredient_nutrients: dict,
                 ingredient_health_labels: List[str]):
        """
        Creates an instance of an Ingredient object
        :param ingredient_name: name of the ingredient
        :param ingredient_id: unique identifier of the ingredient from Edamam
        :param ingredient_img_url: URL to the ingredient image from Edamam
        :param ingredient_nutrients: dictionary containing the ingredient nutritional values
        :param ingredient_health_labels: list containing all ingredient health labels as defined by Edamam
        """
        self.ingredient_name = ingredient_name
        self.ingredient_id = ingredient_id
        self.ingredient_img_url = ingredient_img_url
        self.ingredient_nutrients = ingredient_nutrients
        self.ingredient_health_labels = ingredient_health_labels
