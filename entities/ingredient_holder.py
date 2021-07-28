from threading import Lock

"""
IngredientHolder is part of CoffeeMachine
"""


class IngredientHolder:
    def __init__(self, ingredients=None):
        if ingredients is None:
            ingredients = {}
        self.__ingredients = ingredients
        self.lock = Lock()

    def is_ingredient_supported(self, ingredient: str) -> bool:
        return ingredient in self.__ingredients

    def get_ingredient_quantity(self, ingredient: str) -> int:
        return self.__ingredients.get(ingredient, 0)

    def set_ingredient_quantity(self, ingredient: str, quantity: int) -> None:
        self.__ingredients[ingredient] = quantity
