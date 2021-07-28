"""
Beverage class
"""


class Beverage:
    def __init__(self, name: str):
        self.name = name

    def drink(self):
        print(f"Drinking {self.name}")
