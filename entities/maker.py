import time

import utils.logger as logger
from entities.beverage import Beverage

"""
Multiple BeverageMakers will be part of CoffeeMachine
"""


class BeverageMaker:
    def __init__(self, beverage_name: str, ingredients: dict, make_time_seconds=2):
        self.__beverage_name = beverage_name
        self.__rules = ingredients
        self.__make_time_seconds = make_time_seconds

    def get_composition(self) -> dict:
        return self.__rules

    def get_beverage_name(self) -> str:
        return self.__beverage_name

    """
        Utility function to simulate making of a beverage
        Assuming the beverage takes some time to make , here simulated using sleep
        returns the beverage instance
    """

    def make(self) -> Beverage:
        logger.info(f"{self.__beverage_name} would take {self.__make_time_seconds} seconds")
        time.sleep(self.__make_time_seconds)
        beverage = Beverage(self.__beverage_name)
        logger.info(f"{self.__beverage_name} is prepared")
        return beverage
