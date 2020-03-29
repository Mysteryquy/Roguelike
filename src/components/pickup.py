from dataclasses import dataclass

from src.components.item import Item


@dataclass
class PickUpAction:
    item: Item
    pass
