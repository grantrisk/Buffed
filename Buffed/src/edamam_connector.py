from typing import List

from models import Ingredient, Meal, Measure
import requests


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

    def search_ingredients(self, query) -> List[Ingredient]:
        """
        Queries Food Database API for ingredients. Raises an exception if the API key(s) are invalid.
        :param query: search term
        :return: list of Ingredients from search results
        """
        r = requests.get('https://api.edamam.com/api/food-database/v2/parser',
                         params={'app_id': self.__fd_app_id, 'app_key': self.__fd_app_key,
                                 'ingr': query})
        if r.status_code == 401:
            raise APIKeyError("Invalid food database app ID or key.")

        search_results = []
        food_id = food_name = img_url = ""
        nutrients = {}
        measures = []
        if "hints" in r.json():
            for result in r.json()["hints"]:
                if "foodId" in result["food"]:
                    food_id = result["food"]["foodId"]
                if "label" in result["food"]:
                    food_name = result["food"]["label"]
                if "image" in result["food"]:
                    img_url = result["food"]["image"]
                if "nutrients" in result["food"]:
                    nutrients = result["food"]["nutrients"]
                if "measures" in result:
                    for measure in result["measures"]:
                        measures.append(Measure(measure["label"], measure["uri"],
                                                measure["weight"]))
                food = Ingredient(food_name, food_id, img_url, nutrients, None, measures)
                search_results.append(food)

        return search_results

    def get_ingredient_nutrients(self, ingredient: Ingredient) -> dict:
        """
        Get all nutrients for a given Ingredient. Raises an exception if the Food ID is invalid or API key(s) are invalid.
        :param ingredient: Meal object
        :return: dict containing all nutrients for the given Ingredient
        """
        r = requests.post('https://api.edamam.com/api/food-database/v2/nutrients',
                          params={'app_id': self.__fd_app_id, 'app_key': self.__fd_app_key},
                          json=self.__build_nutrients_json(ingredient.ingredient_id,
                                                           ingredient.ingredient_measures[0].measure_uri))
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 401:
            raise APIKeyError("Invalid food database app ID or key")
        else:
            raise InvalidRequestError("Invalid request: " + r.request.body)

    def search_recipes(self, query) -> List[Meal]:
        """
        Queries Recipe Search API for recipes. Raises an exception if the API key(s) are invalid.
        :param query: search term
        :return: list of Meals from search results
        """
        r = requests.get('https://api.edamam.com/api/recipes/v2',
                         params={'app_id': self.__recipe_app_id, 'app_key': self.__recipe_app_key,
                                 'q': query, 'type': 'public'})
        if r.status_code == 401:
            raise APIKeyError("Invalid food database app ID or key")
        elif r.status_code != 200:
            raise InvalidRequestError("Invalid request")

        search_results = []
        recipe_id = recipe_name = img_url = health_labels = meal_type = ""
        ingredients = []
        nutrients = {}
        if "hits" in r.json():
            for result in r.json()["hits"]:
                if "label" in result["recipe"]:
                    recipe_name = result["recipe"]["label"]
                if "uri" in result["recipe"]:
                    recipe_uri = result["recipe"]["uri"]
                    recipe_id = recipe_uri[recipe_uri.index("#")+1:]
                if "image" in result["recipe"]:
                    img_url = result["recipe"]["image"]
                if "totalNutrients" in result["recipe"]:
                    nutrients = result["recipe"]["totalNutrients"]
                if "healthLabels" in result["recipe"]:
                    health_labels = result["recipe"]["healthLabels"]
                if "ingredients" in result["recipe"]:
                    for ingredient in result["recipe"]["ingredientLines"]:
                        ingredients.append(ingredient)
                if "mealType" in result["recipe"]:
                    meal_type = result["recipe"]["mealType"]

                search_results.append(Meal(recipe_name, recipe_id, nutrients, health_labels, ingredients, meal_type))

        return search_results

    def __build_nutrients_json(self, food_id, measureURI):
        """
        Internal method to build JSON for ingredients input for nutrition input

        :param food_id: food ID fetched from Edamam API
        :return: dict in JSON format containing ingredients in correct format
        """
        return {"ingredients": [
            {
                "quantity": 1,
                "measureURI": measureURI,
                "foodId": food_id
            }
        ]}


class APIKeyError(Exception):
    """
    Exception raised if the provided Edamam API key(s) are invalid
    """
    pass


class InvalidRequestError(Exception):
    """
    General Exception raised if an Edamam API call is invalid
    """
    pass
