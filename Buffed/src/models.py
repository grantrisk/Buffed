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
