from threading import Lock
from typing import List

import utils.logger as logger
from entities.ingredient_holder import IngredientHolder
from entities.maker import BeverageMaker
from utils.locks import CountingLock


class BeverageMachine:
    def __init__(self, outlet_count: int):
        self.__switch_on = False
        self.__outlet_count = outlet_count
        self.__slot_semaphore = CountingLock(outlet_count)  # asyncio.Semaphore(outlet_count)
        self.__ingredient_holder = IngredientHolder()
        self.__beverage_makers = {}
        self.__configure_lock = Lock()  # for machine configuration

    def outlet_count(self) -> int:
        return self.__outlet_count

    def turn_on(self):
        self.__switch_on = True

    def turn_off(self):
        self.__switch_on = False

    def refill_ingredients(self, ingredients: dict):
        for item_name, item_quantity in ingredients.items():
            self.refill_ingredient(item_name, int(item_quantity))

    def refill_ingredient(self, ingredient_name: str, ingredient_quantity: int):
        with self.__ingredient_holder.lock:
            current_quantity = self.__ingredient_holder.get_ingredient_quantity(ingredient_name)
            self.__ingredient_holder.set_ingredient_quantity(ingredient_name, current_quantity + ingredient_quantity)

    def configure_beverage(self, beverage_maker: BeverageMaker):
        with self.__configure_lock:
            self.__beverage_makers[beverage_maker.get_beverage_name()] = beverage_maker
            logger.info(f"configured {beverage_maker.get_beverage_name()}")

    def get_supported_beverages(self) -> List[str]:
        return list(self.__beverage_makers.keys())

    def is_beverage_supported(self, beverage_name: str) -> bool:
        return beverage_name in self.__beverage_makers

    def serve_beverage(self, beverage_name: str):
        logger.info("Request for " + beverage_name)
        if not self.__switch_on:
            logger.warn("Machine is off")
            return None

        with self.__configure_lock:
            if not self.is_beverage_supported(beverage_name):
                logger.warn(f"Beverage {beverage_name} Unsupported")
                return None

        if self.__slot_semaphore.acquire_lock():  # acquire the slot
            with self.__ingredient_holder.lock:
                beverage_composition = self.__beverage_makers[beverage_name].get_composition()
                # check if required quantity of each item is present
                for item, quantity in beverage_composition.items():
                    if not self.__ingredient_holder.is_ingredient_supported(item):
                        logger.error(f"Ingredient {item} for beverage {beverage_name} is not supported by machine")
                        self.__slot_semaphore.release_lock()
                        return None
                    if self.__ingredient_holder.get_ingredient_quantity(item) < quantity:
                        logger.error(f"{beverage_name} cannot be prepared because {item} is not sufficient")
                        self.__slot_semaphore.release_lock()
                        return None

                return self.__make_beverage(beverage_composition, beverage_name)
        else:
            logger.error("No empty slot found for request")
            return None

    def __make_beverage(self, beverage_composition: dict, beverage_name: str):
        for item, quantity in beverage_composition.items():
            current_quantity = self.__ingredient_holder.get_ingredient_quantity(item)
            self.__ingredient_holder.set_ingredient_quantity(item, current_quantity - quantity)
        self.__slot_semaphore.release_lock()
        chosen_maker = self.__beverage_makers[beverage_name]
        return chosen_maker.make()
