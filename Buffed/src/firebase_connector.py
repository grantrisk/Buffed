from typing import List
from models import Meal, User


class FirebaseConnector:
    """
    Provides an interface to fetch data stored in Firebase
    """

    def __init__(self, email: str, password: str, name: str, birthdate: str, gender: str,
                 weight: float, height: float, activity_level: str, active_goal: str, keywords: List[str],
                 allergies: List[str], diet_preferences: List[str], likes: List[str], dislikes: List[str],
                 my_meals: List[Meal], my_goals: List[float, float][float, float][float, float]):
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


    def search_user_database(self, user_email) -> List[User]:
        """
        Queries Firebase for user information. Raises an exception if the email is invalid or not found.
        :param user_email: user's email for searching Firestore database
        :return: list of User objects specific to search query
        """
        pass

    # def get_email(self, user: User) -> str:
    #     """
    #     This method returns the workouts for a user. It raises an exception if the user does not exist.
    #     :param user: the User object for whom you want to get workouts
    #     :return: a List of Workout objects or an empty list if the user has no workouts
    #     """
    #     pass
    #
    # def get_password(self, user: User) -> str:
    #     """
    #     This method returns the workouts for a user. It raises an exception if the user does not exist.
    #     :param user: the User object for whom you want to get workouts
    #     :return: a List of Workout objects or an empty list if the user has no workouts
    #     """
    #     pass

    # def get_login_credentials(self, user: User) -> (str, str):
    #     """
    #     This method returns the workouts for a user. It raises an exception if the user does not exist.
    #     :param user: the User object for whom you want to get workouts
    #     :return: a List of Workout objects or an empty list if the user has no workouts
    #     """
    #     pass

    def get_display_name(self, user: User) -> str:
        """
        The method retrieves the name of the user
        :param user: User object
        :return: name of user
        """
        pass

    def get_user_meals(self, user: User) -> str:
        """
        The method retrieves the meals saved by the user
        :param user: User object
        :return: meals saved by user
        """
        pass

    def get_user_goals(self, user: User) -> str:
        """
        The method retrieves the goals saved by the user
        :param user: User object
        :return: goals saved by user
        """
        pass

    def get_user_diet_info(self, user: User) -> str:
        """
        The method retrieves the diet questionnaire answers by the user
        :param user: User object
        :return: list of answers
        """
        pass

    def get_user_profile_info(self, user: User) -> str:
        """
        The method retrieves the profile preferences saved by the user
        :param user: User object
        :return: list of profile preferences
        """
        pass