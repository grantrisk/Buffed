from typing import List
from models import Meal, User


class FirebaseConnector:
    """
    Provides an interface to fetch data stored in Firebase
    """

    def __init__(self, email: str, password: str, birthdate: str, gender: str,
                 weight: float, height: float, ):
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

    def get_email(self) -> str:
        """
        This method returns the workouts for a user. It raises an exception if the user does not exist.
        :return: a List of Workout objects or an empty list if the user has no workouts
        """
        pass

    def get_password(self) -> str:
        """
        This method returns the workouts for a user. It raises an exception if the user does not exist.
        :return: a List of Workout objects or an empty list if the user has no workouts
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
        This method returns the workouts for a user. It raises an exception if the user does not exist.
        :return: a List of Workout objects or an empty list if the user has no workouts
        """
        pass

    def get_height(self) -> str:
        """
        This method returns the height for a user. It raises an exception if the user does not exist.
        :return: a List of Workout objects or an empty list if the user has no workouts
        """
        pass

    def get_weight(self) -> str:
        """
        This method returns weight for a user. It raises an exception if the user does not exist.
        :return: a List of Workout objects or an empty list if the user has no workouts
        """
        pass

    def get_active_goal(self) -> str:
        """
        This method returns active goal for a user. It raises an exception if the user does not exist.
        :return: a List of Workout objects or an empty list if the user has no workouts
        """
        pass
