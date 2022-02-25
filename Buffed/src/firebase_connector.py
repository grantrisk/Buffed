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
        :param birthdate: user's birthdate for age calculation
        :param gender: user's gender
        :param weight: user's weight in lbs
        :param height: user's height in meters
        :param active_goal: user's active or current goal
        """

    def search_user_database(self, user_email) -> List[User]:
        """
        Queries Firebase for user information. Raises an exception if the email is invalid or not found.
        :param user_email: user's email for searching Firestore database
        :return: list of User objects specific to search query
        """
        pass

    def get_email(self) -> str:
        """
        This method returns the email of a user if one exists.
        :return: A string containing the email of a user.
        """
        pass

    def get_password(self) -> str:
        """
        This method returns the password of a user if one exists.
        :return: A string containing the password of a user.
        """
        pass

    def get_birthdate(self) -> str:
        """
        This method returns the workouts for a user. It raises an exception if the user does not exist.
        :return: a List of Workout objects or an empty list if the user has no workouts
        """
        pass

    def get_gender(self) -> str:
        """
        This method returns the gender of a user, if one exists.
        :return: A string that is the gender of the user.
        """
        pass

    def get_height(self) -> str:
        """
        This method returns the height of a user.
        :return: A string that contains the height of a user.
        """
        pass

    def get_weight(self) -> int:
        """
        This method returns the weight of a user.
        :return: A int that contains the weight of a user.
        """
        pass

    def get_active_goal(self) -> str:
        """
        This method returns active goal for a user. It raises an exception if the user does not exist.
        :return: A string containing the active goal for the user.
        """
        pass