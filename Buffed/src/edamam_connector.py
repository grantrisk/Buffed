import models


class EdamamConnector:
    """
    Provides an interface to fetch Edamam API data
    """
    def __init__(self, fd_app_id: str, fd_app_key: str,
                 recipe_app_id: str, recipe_app_key: str,
                 na_app_id: str, na_app_key: str):
        """
        Creates an instance of NutritionCollector.

        :param fd_app_id: App ID for Food Database API
        :param fd_app_key: App key for Food Database API
        :param recipe_app_id: App ID for Recipe Search API
        :param recipe_app_key: App key for Recipe Search API
        :param na_app_id: App ID for Nutritional Analysis API
        :param na_app_key: App Key for Nutritional Analysis API
        """
        self.__fd_app_id = fd_app_id
        self.__fd_app_key = fd_app_key
        self.__recipe_app_id = recipe_app_id
        self.__recipe_app_key = recipe_app_key
        self.__na_app_id = na_app_id
        self.__na_app_key = na_app_key

    def search_food_database(self, query):
        """
        Queries Food Database API for foods and ingredients. Raises an exception if the API key(s) are invalid.
        :param query: search term
        :return: list of Meals containing search results
        """
        pass

    def get_food_nutrients(self, meal: models.Meal):
        """
        Get all nutrients for a given Meal. Raises an exception if the Food ID is invalid or API key(s) are invalid.
        :param meal: Meal object
        :return: dict containing all nutrients for the given Meal
        """
        pass
