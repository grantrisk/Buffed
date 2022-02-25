from typing import List


class Ingredient:
    def __init__(self, food_name: str, food_id: str, img_url: str, nutrients: dict, health_labels: List[str]):
        """
        Creates an instance of a Food object
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


class Meal:
    def __init__(self, meal_name: str, meal_id: str, nutrients: dict, health_labels: List[str],
                 ingredients: List[Ingredient], meal_type: str):
        """
        Creates an instance of a Meal object
        :param meal_name: name of the meal
        :param meal_id: unique identifier for the Meal
        :param nutrients: dictionary containing all nutrients
        :param health_labels: list containing all health labels as defined by Edamam
        :param ingredients: list containing all ingredients in the meal
        :param meal_type: type of meal (i.e. Breakfast, Lunch, Dinner, etc.)
        """
        self.meal_name = meal_name
        self.meal_id = meal_id
        self.nutrients = nutrients
        self.health_labels = health_labels
        self.ingredients = ingredients
        self.meal_type = meal_type


class MealPlan:
    def __init__(self, meals: List[Meal], meal_plan_id: str, description=None):
        """
        Creates an instance of a MealPlan object (Today's Plan)
        :param meals: list of meals for one day
        :param meal_plan_id: unique identifier for MealPlan stored in Firebase
        :param description: optional description for MealPlan
        """
        self.meals = meals
        self.meal_plan_id = meal_plan_id
        self.description = description


class Goal:
    def __init__(self, goal_id: str, goal_name: str, isActive: bool, calories: int, macro_nutrients: dict,
                 number_of_meals: int, desired_weight: int):
        """
        Creates an instance of a Goal object
        :param goal_id: unique identifier for Goal stored in Firebase
        :param goal_name: name of the goal
        :param isActive: determines active goal
        :param calories: daily calorie amount to achieve
        :param macro_nutrients: dictionary containing protein, fat, and carb amounts (g)
        :param number_of_meals: number of desired meals per day
        :param desired_weight: desired weight to achieve (lbs)
        """
        self.goal_id = goal_id
        self.goal_name = goal_name
        self.isActive = isActive
        self.calories = calories
        self.macro_nutrients = macro_nutrients
        self.number_of_meals = number_of_meals
        self.desired_weight = desired_weight


class User:
    def __init__(self, email: str, password: str, name: str, birthdate: str, gender: str,
                 weight: float, height: float, activity_level: str, active_goal: Goal, keywords: List[str],
                 allergies: List[str], diet_preferences: List[str], likes: List[str], dislikes: List[str],
                 my_meals: List[Meal], meal_plan: MealPlan, my_goals: List[Goal]):
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
        self.meal_plan = meal_plan
        self.my_goals = my_goals
