from typing import List

from models import Ingredient, Meal, Measure
import requests


class EdamamConnector:
    """
    Provides an interface to fetch Edamam API data
    """
    config = {}
    with open('static/resources/keys.cfg') as file:
        lines = file.readlines()
        for line in lines:
            key_val = line.split('=')
            config[key_val[0].strip()] = key_val[1].strip()

    def __init__(self):
        """
        Creates an instance of EdamamConnector.
        """
        self.__fd_app_id = EdamamConnector.config['fd_app_id']
        self.__fd_app_key = EdamamConnector.config['fd_app_key']
        self.__recipe_app_id = EdamamConnector.config['recipe_app_id']
        self.__recipe_app_key = EdamamConnector.config['recipe_app_key']
        self.__na_app_id = EdamamConnector.config['na_app_id']
        self.__na_app_key = EdamamConnector.config['na_app_key']

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

    def search_recipes(self, query: str, diet: dict) -> List[Meal]:
        """
        Queries Recipe Search API for recipes. Raises an exception if the API key(s) are invalid.
        :param query: search term
        :param filters: dict containing key-value filter parameters
        :param diet: dict containing dietary/allergy/nutrient filters (must use Edamam API parameter labels)
        :return: list of Meals from search results
        """
        params = {'app_id': self.__recipe_app_id, 'app_key': self.__recipe_app_key, 'q': query, 'type': 'public'}
        params.update(diet)

        r = requests.get('https://api.edamam.com/api/recipes/v2', params=params)
        if r.status_code == 401:
            raise APIKeyError("Invalid food database app ID or key")
        elif r.status_code != 200:
            raise InvalidRequestError("Invalid request")

        search_results = []
        recipe_id, recipe_name, img_url, health_labels, meal_type, recipe_source, recipe_url = "", "", "", "", "", "", ""
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
                    nutrients["ENERC_KCAL"]["quantity"] /= result["recipe"]["yield"]
                if "healthLabels" in result["recipe"]:
                    health_labels = result["recipe"]["healthLabels"]
                if "ingredients" in result["recipe"]:
                    for ingredient in result["recipe"]["ingredientLines"]:
                        ingredients.append(ingredient)
                if "mealType" in result["recipe"]:
                    meal_type = result["recipe"]["mealType"]
                if "source" in result["recipe"]:
                    recipe_source = result["recipe"]["source"]
                if "url" in result["recipe"]:
                    recipe_url = result["recipe"]["url"]

                search_results.append(Meal(recipe_name, recipe_id, None, img_url, nutrients, health_labels, ingredients,
                                           meal_type, recipe_source, recipe_url))

        return search_results

    def get_recipe_by_id(self, recipe_id):
        r = requests.get('https://api.edamam.com/api/recipes/v2/' + recipe_id,
                         params={'app_id': self.__recipe_app_id, 'app_key': self.__recipe_app_key,
                                 'type': 'public'})

        nutrients = {}
        ingredients = []
        recipe_name, img_url, health_labels, meal_type, recipe_source, recipe_url = "", "", "", "", "", ""
        if "recipe" in r.json():
            recipe = r.json()["recipe"]
            if "label" in recipe:
                recipe_name = recipe["label"]
            if "totalNutrients" in recipe:
                nutrients = recipe["totalNutrients"]
                for nutrient in nutrients:
                    nutrients[nutrient]["quantity"] /= recipe["yield"]
            if "image" in recipe:
                img_url = recipe["image"]
            if "healthLabels" in recipe:
                health_labels = recipe["healthLabels"]
            if "mealType" in recipe:
                meal_type = recipe["mealType"]
            if "ingredientLines" in recipe:
                ingredients = recipe["ingredientLines"]
            if "source" in recipe:
                recipe_source = recipe["source"]
            if "url" in recipe:
                recipe_url = recipe["url"]

            return Meal(recipe_name, recipe_id, None, img_url, nutrients, health_labels, ingredients, meal_type,
                        recipe_source, recipe_url)

    def is_valid_image(self, img_url: str):
        """
        Determines whether the requested Edamam image has expired.
        :param img_url: URL of the requested image
        :return: True if valid, False otherwise
        """
        r = requests.get(img_url)
        return r.status_code in (200, 304)


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
