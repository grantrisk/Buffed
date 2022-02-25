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


class User:
    def __init__(self, email: str, password: str, name: str, birthdate: str, gender: str,
                 weight: float, height: float, activity_level: str, active_goal: str, keywords: List[str],
                 allergies: List[str], diet_preferences: List[str], likes: List[str], dislikes: List[str],
                 my_meals: List[Meal], my_goals: List[float,float][float,float][float,float] ):
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
