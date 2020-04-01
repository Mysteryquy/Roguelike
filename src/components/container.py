from dataclasses import dataclass
from typing import List


@dataclass
class Container:
    """ used for entities that are containers """

    def __init__(self, inventory=None, volume=10.0, gold=0):
        if not inventory:
            self.inventory = []
        else:
            self.inventory = inventory
        self.max_volume = volume
        self._volume = 0.0
        self.gold = gold
